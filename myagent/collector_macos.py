import psutil
import platform
import subprocess


def macos_info(self):
    from myagent.collector import safe_get
    psutils_pro = psutil.Process()

    info = {}

    info["sysctl"] = safe_get(subprocess.run(['sysctl', '-n', 'hw.model'], capture_output=True, text=True).stdout.lower)
    info["hypervisor"] = safe_get(subprocess.run(["sysctl", '-n', "machdep.cpu.features"], capture_output=True, text=True).stdout.lower)

    self.report["macos_info"] = info

    '''self.report["macos_info"] = {
        "cpu_percent": psutils_pro.cpu_percent(),
        "cpu_times": psutils_pro.cpu_times(),
        "memory_info": psutils_pro.memory_info(),
        "memory_percent": psutils_pro.memory_percent(),
        "num_ctx_switches": psutils_pro.num_ctx_switches(),
        "num_threads": psutils_pro.num_threads(),
        "create_time": psutils_pro.create_time(),
        "gids": psutils_pro.gids(),
        "name": psutils_pro.name(),
        "ppid": psutils_pro.ppid(),
        "status": psutils_pro.status(),
        "terminal": psutils_pro.terminal(),
        "uids": psutils_pro.uids(),
        "username": psutils_pro.username(),
        "platform": platform.mac_ver(),
    }'''
