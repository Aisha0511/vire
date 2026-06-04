import os
import distro

def linux_info(self):
    from myagent.collector import safe_get, safe_run, safe_read_dir_files, safe_read_file

    info = {}

    base_find = ["find", "/", "-xdev", "-maxdepth", "8"]

    info["suid_files"] = safe_run(base_find + ["-perm", "-4000", "-type", "f"], timeout=30)
    info["sgid_files"] = safe_run(base_find + ["-perm", "-2000", "-type", "f"], timeout=30)
    info["world_writable_files"] = safe_run(base_find + ["-perm", "-o+w", "-type", "f", "-not", "-path", "*/proc/*"], timeout=30)
    info["world_writable_dirs"] = safe_run(base_find + ["-perm", "-o+w", "-type", "d", "-not", "-path", "*/proc/*"], timeout=30)
    info["no_owner_files"] = safe_run(base_find + ["-nouser"], timeout=30)
    info["last_logins"] = safe_run(["last", "-n", "50"])
    info["lastlog"] = safe_run(["lastlog"])
    info["failed_logins"] = safe_run(["lastb", "-n", "20"])
    info["who"] = safe_run(["who"])
    info["w"] = safe_run(["w"])
    info["sudoers_file"] = safe_read_file("/etc/sudoers")
    info["sudoers_dir"] = safe_read_dir_files("/etc/sudoers.d")
    info["virt_detect"] = safe_run(["systemd-detect-virt"])
    info["kernel_version"] = safe_run(["uname", "-r"])
    info["kernel_cmdline"] = safe_read_file("/proc/cmdline")
    info["systemd_services"] = safe_run(["systemctl", "list-units", "--type=service", "--all", "--no-pager"])
    info["failed_services"] = safe_run(["systemctl", "--failed", "--no-pager"])
    info["sshd_config"] = safe_read_file("/etc/ssh/sshd_config")
    info["ssh_host_keys"] = safe_run(["ls", "-la", "/etc/ssh/"])
    info["authorized_keys_root"] = safe_read_file("/root/.ssh/authorized_keys")
    info["lsof_network"] = safe_run(["lsof", "-i", "-n", "-P"], timeout=15)
    info["routes"] = safe_run(["ip", "route"]) or safe_run(["netstat", "-rn"])
    info["iptables_v4"] = safe_run(["iptables", "-L", "-n", "-v"])
    info["iptables_v6"] = safe_run(["ip6tables", "-L", "-n", "-v"])
    info["ufw_status"] = safe_run(["ufw", "status", "verbose"])
    info["nftables"] = safe_run(["nft", "list", "ruleset"])
    
    if os.path.exists("/usr/bin/dpkg") or os.path.exists("/bin/dpkg"):
        info["installed_packages"] = safe_run(["dpkg", "-l"], timeout=30)
    elif os.path.exists("/usr/bin/rpm"):
        info["installed_packages"] = safe_run(["rpm", "-qa", "--qf", "%{NAME} %{VERSION}-%{RELEASE}\n"], timeout=30)
    elif os.path.exists("/usr/bin/pacman"):
        info["installed_packages"] = safe_run(["pacman", "-Q"], timeout=30)
    else:
        info["installed_packages"] = {"error": "no known package manager"}

    try:
        info["distro_data"] = distro.info()
    except ImportError:
        info["distro_data"] = {"error": "distro not founded"}

    if os.path.exists("/usr/bin/apt-get"):
        info["security_updates"] = safe_run(["apt-get", "--just-print", "upgrade"], timeout=30)
    elif os.path.exists("/usr/bin/yum"):
        info["security_updates"] = safe_run(["yum", "check-update", "--security"], timeout=30)

    self.report["linux_info"] = info
    
