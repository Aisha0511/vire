import psutil
import platform
import subprocess


def windows_info(self):
    from myagent.collector import safe_get
    psutils_pro = psutil.Process()

    info = {}

    info["wmic"] = safe_get(subprocess.run(['wmic', 'computersystem', 'get', 'model'], capture_output=True, text=True).stdout.lower)

    self.report["windows_info"] = info

    '''self.report["windows_info"] = {
        "cpu_percent": psutils_pro.cpu_percent(),
        "cpu_times": psutils_pro.cpu_times(),
        "io_counters": psutils_pro.io_counters(),
        "memory_info": psutils_pro.memory_info(),
        "memory_maps": psutils_pro.memory_maps(),
        "num_ctx_switches": psutils_pro.num_ctx_switches(),
        "num_threads": psutils_pro.num_threads(),
        "username": psutils_pro.username(),
        "exe": psutils_pro.exe(),
        "name": psutils_pro.name(),
        "platform": platform.win32_ver(),
    }'''
