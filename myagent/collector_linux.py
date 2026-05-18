import psutil
import platform

def linux_info(self):
    psutils_pro = psutil.Process()

    self.report['linux_info'] = {
                "running_on_cpu": psutils_pro.cpu_num(),
                "cpu_percent": psutils_pro.cpu_percent(),
                "cpu_times": psutils_pro.cpu_times(),
                "create_time": psutils_pro.create_time(),
                "name": psutils_pro.name(),
                "ppid": psutils_pro.ppid(),
                "status": psutils_pro.status(),
                "terminal": psutils_pro.terminal(),
                "gids": psutils_pro.gids(),
                "num_ctx_switches": psutils_pro.num_ctx_switches(),
                "uids": psutils_pro.uids(),
                "username": psutils_pro.username(),
                "memory_full_info": psutils_pro.memory_full_info(),
                "memory_maps": psutils_pro.memory_maps(),
                "platform": platform.freedesktop_os_release(),
            }

