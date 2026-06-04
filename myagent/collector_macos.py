
def macos_info(self):
    from myagent.collector import safe_get, safe_run, safe_read_file, safe_read_dir_files

    info = {}

    base_find = ["find", "/", "-xdev", "-maxdepth", "8"]

    info["suid_files"] = safe_run(base_find + ["-perm", "-4000", "-type", "f"], timeout=30)
    info["sgid_files"] = safe_run(base_find + ["-perm", "-2000", "-type", "f"], timeout=30)
    info["world_writable_files"] = safe_run(base_find + ["-perm", "-o+w", "-type", "f", "-not", "-path", "*/proc/*"], timeout=30)
    info["world_writable_dirs"] = safe_run(base_find + ["-perm", "-o+w", "-type", "d", "-not", "-path", "*/proc/*"], timeout=30)
    info["no_owner_files"] = safe_run(base_find + ["-nouser"], timeout=30)
    info["last_logins"] = safe_run(["last", "-n", "50"])
    info["lastlog"] = safe_run(["lastlog"])
    info["failed_logins"] = safe_run(["lastb", "-n", "20"])
    info["who"] = safe_run(["who"])
    info["w"] = safe_run(["w"])
    info["sudoers_file"] = safe_read_file("/etc/sudoers")
    info["sudoers_dir"] = safe_read_dir_files("/etc/sudoers.d")
    info["hw_model"] = safe_run(["sysctl", "-n", "hw.model"])
    info["cpu_features"] = safe_run(["sysctl", "-n", "machdep.cpu.features"])
    info["sw_vers"] = safe_run(["sw_vers"])
    info["brew_packages"] = safe_run(["brew", "list", "--versions"], timeout=30)
    info["brew_outdated"] = safe_run(["brew", "outdated"], timeout=30)
    info["sshd_config"]  = safe_read_file("/etc/ssh/sshd_config")
    info["authorized_keys_root"] = safe_read_file("/var/root/.ssh/authorized_keys")
    info["pf_rules"] = safe_run(["pfctl", "-sr"])
    info["pf_status"] = safe_run(["pfctl", "-si"])
    info["dscl_users"]   = safe_run(["dscl", ".", "-list", "/Users"])
    info["last_logins"]  = safe_run(["last", "-20"])
    info["routes"] = safe_run(["ip", "route"]) or safe_run(["netstat", "-rn"])

    self.report["macos_info"] = info

