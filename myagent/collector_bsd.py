import psutil
import distro


def bsd_info(self):
    psutils_pro = psutil.Process()

    self.report["bsd_info"] = {
        "distro_info": distro.info(),
        "cpu_num": psutils_pro.cpu_num(),
        "cpu_percent": psutils_pro.cpu_percent(),
        "cpu_times": psutils_pro.cpu_times(),
        "create_time": psutils_pro.create_time(),
        "gids": psutils_pro.gids(),
        "io_counters": psutils_pro.io_counters(),
        "name": psutils_pro.name(),
        "memory_info": psutils_pro.memory_info(),
        "memory_percent": psutils_pro.memory_percent(),
        "num_ctx_switches": psutils_pro.num_ctx_switches(),
        "ppid": psutils_pro.ppid(),
        "status": psutils_pro.status(),
        "terminal": psutils_pro.terminal(),
        "uids": psutils_pro.uids(),
        "username": psutils_pro.username(),
    }
