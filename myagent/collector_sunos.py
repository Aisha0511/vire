import psutil

def sunos_info(self):
    self.report['sunos_info'] = {
                "name": psutil.Process().name(),
                "cmdline": psutil.Process().cmdline(),
                "create_time": psutil.Process().create_time(),
                "memory_info": psutil.Process().memory_info(),
                "memory_percent": psutil.Process().memory_percent(),
                "num_threads": psutil.Process().num_threads(),
                "ppid": psutil.Process().ppid(),
                "status": psutil.Process().status(),
                "terminal":psutil.Process().terminal(),
                "gids": psutil.Process().gids(),
                "uids": psutil.Process().uids(),
                "username": psutil.Process().username()
            }