import psutil
import platform

def windows_info(self):
    self.report['windows_info'] = {
                "cpu_percent": psutil.Process().cpu_percent(),
                "cpu_times": psutil.Process().cpu_times(),
                "io_counters": psutil.Process().io_counters(),
                "memory_info": psutil.Process().memory_info(),
                "memory_maps": psutil.Process().memory_maps(),
                "num_ctx_switches": psutil.Process().num_ctx_switches(),
                "num_threads": psutil.Process().num_threads(),
                "username": psutil.Process().username(),
                "exe": psutil.Process().exe(),
                "name": psutil.Process().name(),
                "platform": platform.win32_ver(),
            }