import psutil
import distro

def aix_info(self):
    psutils_pro = psutil.Process()

    self.report["aix_info"] = {
        "distro_info": distro.info(),
        "name": psutils_pro.name(),
        "cmdline": psutils_pro.cmdline(),
        "create_time": psutils_pro.create_time(),
        "memory_info": psutils_pro.memory_info(),
        "memory_percent": psutils_pro.memory_percent(),
        "num_threads": psutils_pro.num_threads(),
        "ppid": psutils_pro.ppid(),
        "status": psutils_pro.status(),
        "terminal": psutils_pro.terminal(),
        "gids": psutils_pro.gids(),
        "uids": psutils_pro.uids(),
        "username": psutils_pro.username(),
    }
