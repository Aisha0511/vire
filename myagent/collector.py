import socket
import psutil 
import platform 
from .collector_linux import linux_info
from .collector_windows import windows_info
from .collector_macos import macos_info
from .collector_bsd import bsd_info
from .collector_aix import aix_info
from .collector_sunos import sunos_info
from .collector_other import other_info


class Collector:
    def __init__(self):
        self.report = {}
        self.os = platform.system()

    def collect_system_info(self):
        self.report['system_info'] = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "architecture": platform.architecture(),
            "machine": platform.machine(),     
        }

    def collect_os_info(self):
        if  self.os == "Linux":
            linux_info(self)
        elif self.os == "Windows":
            windows_info(self)
        elif self.os == "macOS":
            macos_info(self)
        elif self.os == "BSD":
            bsd_info(self)
        elif self.os == "SunOS":
            sunos_info(self)
        elif self.os == "AIX":
            aix_info(self)
        else:
            other_info(self)

    def collect_process_info(self):
        self.report['process_info'] = {
            "total_cpu": psutil.cpu_times()._asdict(),
            "cpu_times": psutil.cpu_times()._asdict(),
            "cpu_usage_percent": psutil.cpu_percent(interval=1),
            "cpu_usage_each": psutil.cpu_percent(percpu=True),
            "cpu_count_all": psutil.cpu_count(logical=True),
            "cpu_count_physical": psutil.cpu_count(logical=False),
            "cpu_status": psutil.cpu_stats()._asdict(),
            "cpu_frequencies": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            "virtual_memory": psutil.virtual_memory()._asdict(),
            "swap.memory": psutil.swap_memory()._asdict(),
            "disk_partitions": psutil.disk_partitions(),
            "disk_usage": psutil.disk_usage('/')._asdict(),
            "disk_io_counters": psutil.disk_io_counters()._asdict(),
            "io_counters": psutil.net_io_counters(pernic=True),
            "connections": psutil.net_connections(),
            "interfaces": psutil.net_if_addrs(),
            "nic_stats": psutil.net_if_stats(),
            "temperatures": psutil.sensors_temperatures(),
            "fans": psutil.sensors_fans(),
            "battery": psutil.sensors_battery()._asdict(),
            "users": psutil.users(),
            "running_process": [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'username', 'status'])],
        }

    def collect_ports_info(self):
        ports = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'LISTEN':
                process_name = None
                process_cmd = None
                protocol = 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
                if conn.status == psutil.CONN_LISTEN or protocol == 'UDP' or conn.status == psutil.CONN_ESTABLISHED:
                    if conn.pid:
                        try:
                            proc = psutil.Process(conn.pid)
                            process_name = proc.name()
                            process_cmd  = ' '.join(proc.cmdline())
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            process_name = 'unknown'
                    ports.append({
                        'port': conn.laddr.port,
                        'ip': conn.laddr.ip,
                        'pid': conn.pid,
                        'process': process_name,
                        'cmdline': process_cmd,
                        'protocol': protocol,
                        'status': conn.status
                    })
        ports = sorted(ports, key=lambda x: x['port'])
        self.report['ports_info'] = {
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "open_ports": ports
        }

    def collect_info(self):
        self.collect_system_info()
        self.collect_os_info()
        self.collect_process_info()
        self.collect_ports_info()
        
        return self.report

