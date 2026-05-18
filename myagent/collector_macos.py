import psutil
import platform

def macos_info(self):
    self.report['macos_info'] = {
                "cpu_percent": psutil.Process().cpu_percent(),
                "cpu_times": psutil.Process().cpu_times(),
                "memory_info": psutil.Process().memory_info(),
                "memory_percent": psutil.Process().memory_percent(),
                "num_ctx_switches": psutil.Process().num_ctx_switches(),
                "num_threads": psutil.Process().num_threads(),
                "create_time": psutil.Process().create_time(),
                "gids": psutil.Process().gids(),
                "name": psutil.Process().name(),
                "ppid": psutil.Process().ppid(),
                "status": psutil.Process().status(),
                "terminal": psutil.Process().terminal(),
                "uids": psutil.Process().uids(),
                "username": psutil.Process().username(),
                "platform": platform.mac_ver(),
            }