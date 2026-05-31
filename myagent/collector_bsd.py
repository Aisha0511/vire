import psutil
import distro


def bsd_info(self):
    from myagent.collector import safe_get, safe_run, safe_read_file, safe_read_dir_files

    info = {}
    info["uname_a"] = safe_run(["uname", "-a"])
    info["sysctl_all"] = safe_run(["sysctl", "-a"], timeout=15)
    info["pkg_list"] = safe_run(["pkg", "info"])
    info["pf_rules"] = safe_run(["pfctl", "-sr"])
    info["crontab_root"] = safe_run(["crontab", "-l"])
    info["sshd_config"] = safe_read_file("/etc/ssh/sshd_config")
    info["hosts_file"] = safe_read_file("/etc/hosts")
    self.report["bsd_info"] = info
