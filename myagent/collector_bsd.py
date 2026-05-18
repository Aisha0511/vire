import psutil

def bsd_info(self):
    self.report['bsd_info'] = {
                "cpu_num": psutil.Process().cpu_num(),
                "cpu_percent": psutil.Process().cpu_percent(),
                "cpu_times": psutil.Process().cpu_times(),
                "create_time": psutil.Process().create_time(),
                "gids": psutil.Process().gids(),
                "io_counters": psutil.Process().io_counters(),
                "name": psutil.Process().name(),
                "memory_info": psutil.Process().memory_info(),
                "memory_percent": psutil.Process().memory_percent(),
                "num_ctx_switches": psutil.Process().num_ctx_switches(),
                "ppid": psutil.Process().ppid(),
                "status": psutil.Process().status(),
                "terminal": psutil.Process().terminal(),
                "uids": psutil.Process().uids(),
                "username": psutil.Process().username()
            }