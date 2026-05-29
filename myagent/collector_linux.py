import psutil
import platform
import distro
import subprocess



def linux_info(self):
    from myagent.collector import safe_get
    psutils_pro = psutil.Process()

    info = {}

    info["distro"] = safe_get(distro.info)
    info["virt_detect"] = safe_get(subprocess.run(['systemd-detect-virt'], capture_output=True, text=True, check=True).stdout.strip)
    #info["suid"] = safe_get(subprocess.run(["find", "/", "-xdev", "-perm", "-4000", "-type", "f"], stdout=subprocess.PIPE, text=True, stderr=subprocess.DEVNULL, timeout=60))


    
    self.report["linux_info"] = info

    '''self.report["linux_info"] = {
        "distro_info": distro.info(),

        "running_on_cpu": psutils_pro.cpu_num(),
        "cpu_percent": psutils_pro.cpu_percent(),
        "cpu_times": psutils_pro.cpu_times(),
        "create_time": psutils_pro.create_time(),
        "name": psutils_pro.name(),
        "ppid": psutils_pro.ppid(),
        "status": psutils_pro.status(),
        "terminal": psutils_pro.terminal(),
        "gids": psutils_pro.gids()._asdict(),
        "num_ctx_switches": psutils_pro.num_ctx_switches()._asdict(),
        "uids": psutils_pro.uids()._asdict(),
        "username": psutils_pro.username(),
        "memory_full_info": psutils_pro.memory_full_info()._asdict(),
        "memory_maps": psutils_pro.memory_maps(),
        "platform": platform.freedesktop_os_release(),
        "last_50": subprocess.run(
            ["last", "-n", "50"], capture_output=True, text=True
        ).stdout,
        "lastlog": subprocess.run(["lastlog"], capture_output=True, text=True).stdout,'''
    
