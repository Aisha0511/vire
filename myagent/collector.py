import socket
import psutil 
import platform 
import subprocess
import os
import pwd
import grp
from .collector_linux import linux_info
from .collector_windows import windows_info
from .collector_macos import macos_info
from .collector_bsd import bsd_info
from .collector_aix import aix_info
from .collector_sunos import sunos_info
from .collector_other import other_info

def safe_get(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        if hasattr(result, '_asdict'):
            return result._asdict()
        return result
    except Exception as e:
        return {"error": str(e)}
        
def safe_run(cmd, timeout=60):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=timeout)
        return result.stdout.strip().splitlines()
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except FileNotFoundError:
        return {"error": f"command not found: {cmd[0]}"}
    except Exception as e:
        return {"error": str(e)}
    
def safe_read_file(path):
    try:
        with open(path, 'r', errors='replace') as f:
            return f.read()
    except Exception as e:
        return {"error": str(e)}
    
def safe_read_dir_files(directory, extensions=None, max_files=50):
    result = {}
    if not os.path.isdir(directory):
        return {"error": f"directory not found: {directory}"}
    count = 0
    for root, _, files in os.walk(directory):
        for fname in files:
            if extensions and not any(fname.endswith(e) for e in extensions):
                continue
            fpath = os.path.join(root, fname)
            result[fpath] = safe_read_file(fpath)
            count += 1
            if count >= max_files:
                result["read_directory_files"] = f"stopped at {max_files} files"
            return result
    return result
        
class Collector:
    def __init__(self):
        self.report = {}
        self.os = platform.system()

    def collect_system_info(self):
        p = platform
        psutils = psutil

        info = {}

        info["uname"] = safe_get(p.uname)
        info["platform"] = safe_get(p.platform)
        info["architecture"] = safe_get(p.architecture)
        info["boot_time"] = safe_get(psutils.boot_time)
        info["cpu_times"] = safe_get(psutils.cpu_times)
        info["cpu_usage_percent"] = safe_get(psutils.cpu_percent, interval=1)
        info["cpu_usage_each"] = safe_get(psutils.cpu_percent, interval=1, percpu=True)
        info["cpu_count_all"] = safe_get(psutils.cpu_count, logical=True)
        info["cpu_count_physical"] = safe_get(psutils.cpu_count, logical=False)
        info["cpu_status"] = safe_get(psutils.cpu_stats)
        info["cpu_frequencies"] = safe_get(psutils.cpu_freq)
        info["virtual_memory"] = safe_get(psutils.virtual_memory)
        info["swap_memory"] = safe_get(psutils.swap_memory)

        info["temperatures"] = safe_get(psutils.sensors_temperatures) if hasattr(psutils, "sensors_temperatures") else None
        info["fans"] = safe_get(psutils.sensors_fans) if hasattr(psutils, "sensors_fans") else None
        info["battery"] = safe_get(psutils.sensors_battery) if hasattr(psutils, "sensors_battery") else None
        info["users"] = safe_get(psutils.users)

        info["suid"] = safe_run(["find", "/", "-xdev", "-perm", "-4000", "-type", "f"])
        info["sgid"] = safe_run(["find", "/", "-xdev", "-perm", "-2000", "-type", "f"])
        info["world_writable_files"] = safe_run(["find", "/", "-xdev", "-perm", "-o+w", "-type", "f"])
        info["world_writable_dirs"] = safe_run(["find", "/", "-xdev", "-perm", "-o+w", "-type", "d"])
        info["no_owner"] = safe_run(["find", "/", "-xdev", "-nouser", "-o", "-nogroup"])

        try:
            info["disk_partitions"] = [
                {
                    **part._asdict(),
                    "usage": safe_get(psutils.disk_usage, part.mountpoint)
                }
                for part in psutils.disk_partitions(all=True)
            ]
        except Exception as e:
            info["disk_partitions"] = {"error": str(e)}

        try:
            counters = psutils.disk_io_counters(perdisk=True)
            info["disk_io_counters"] = {
                disk: c._asdict() for disk, c in counters.items()
            } if counters else None
        except Exception as e:
            info["disk_io_counters"] = {"error": str(e)}

        try:
            info["running_processes"] = [
                proc.info for proc in psutils.process_iter(
                    attrs=['pid', 'name', 'username', 'status', 'cmdline', 'exe', 'ppid', 'create_time']
                )
            ]
        except Exception as e:
            info["running_processes"] = {"error": str(e)}

        self.report['system_info'] = info

    def collect_users_info(self):
        info = {}

        try:
            HAS_PWD = True
            if HAS_PWD:
                info["passwords"] = [list(u) for u in pwd.getpwall()]
                info["groups"] = [list(g) for g in grp.getgrall()]
                info["uid0_users"] = [list(u) for u in pwd.getpwall() if u.pw_uid == 0]
                info["no_password_users"] = [list(u) for u in pwd.getpwall() if u.pw_passwd == '']
        except Exception as e:
            info["has_pwd"] = {"error": str(e)}

        self.report['users_info'] = info

    def collect_os_info(self):
        if  self.os == "Linux":
            linux_info(self)
        elif self.os == "Windows":
            windows_info(self)
        elif self.os == "Darwin":
            macos_info(self)
        elif self.os in ("FreeBSD", "OpenBSD", "NetBSD"):
            bsd_info(self)
        elif self.os == "SunOS":
            sunos_info(self)
        elif self.os == "AIX":
            aix_info(self)
        else:
            self.report["os_info"] = {"os": self.os, "note": "not founded"}

    def collect_net_info(self):
        psutils = psutil
        
        info = {}

        info["net_io_counters"] = safe_get(psutils.net_io_counters, pernic=True)
        info["interfaces"] = safe_get(psutils.net_if_addrs)
        info["net_status"] = safe_get(psutils.net_if_stats)
        info["connections"] = safe_get(psutils.net_connections)
        info["hostname_full"] = socket.getfqdn()

        self.report['net_info'] = info

    def collect_ports_info(self):
        ports = []

        try:
            for conn in psutil.net_connections(kind='tcp'):
                if conn.status == psutil.CONN_LISTEN:
                    continue
                process_name = None
                process_cmd = None
                
                if conn.pid:
                    try:
                        proc = psutil.Process(conn.pid)
                        process_name = proc.name()
                        process_cmd = ' '.join(proc.cmdline())
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        process_name = 'unknown'
                        process_cmd = 'unknown'

                ports.append({
                    'port': conn.laddr.port,
                    'ip': conn.laddr.ip,
                    'pid': conn.pid,
                    'process': process_name,
                    'cmdline': process_cmd,
                    'protocol': 'TCP',
                    'status': conn.status
                })
        except Exception as e:
            ports.append({"error_tcp": str(e)})

        try:
            for conn in psutil.net_connections(kind='udp'):
                if not conn.laddr or conn.laddr.port == 0:
                    continue
                process_name = None
                process_cmd = None

                if conn.pid:
                    try:
                        proc = psutil.Process(conn.pid)
                        process_name = proc.name()
                        process_cmd = ' '.join(proc.cmdline())
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        process_name = 'unknown'
                        process_cmd = 'unknown'

                ports.append({
                    'port': conn.laddr.port,
                    'ip': conn.laddr.ip,
                    'pid': conn.pid,
                    'process_name': process_name,
                    'cmdline': process_cmd,
                    'protocol': 'UDP',
                    'status': 'LISTEN'
                })
        except Exception as e:
            ports.append({"error_udp": str(e)})

        ports = sorted(
            [p for p in ports if 'port' in p],
            key=lambda x: x['port']
        )

        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            domain_name = socket.getfqdn(ip_address)
        except Exception as e:
            hostname = {"error": str(e)}
            ip_address = None
            domain_name = None

        self.report['ports_info'] = {
            "open_ports": ports,
            "hostname": hostname,
            "ip_address": ip_address,
            "domain_name": domain_name,
        }

    def collect_info(self):
        self.collect_system_info()
        self.collect_users_info()
        self.collect_os_info()
        self.collect_net_info()
        self.collect_ports_info()
        
        return self.report
