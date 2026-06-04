
def windows_info(self):
    from myagent.collector import safe_get, safe_run, safe_read_file, safe_read_dir_files

    info = {}

    info["computer_model"] = safe_run(["wmic", "computersystem", "get", "model", "/value"])
    info["os_version"] = safe_run(["wmic", "os", "get", "caption,version,buildnumber", "/value"])
    info["installed_software"] = safe_run(["wmic", "product", "get", "name,version", "/value"], timeout=60)
    info["services"] = safe_run(["sc", "query", "type=", "all", "state=", "all"])
    info["local_users"] = safe_run(["net", "user"])
    info["local_groups"] = safe_run(["net", "localgroup"])
    info["admins"] = safe_run(["net", "localgroup", "Administrators"])
    info["firewall_rules"] = safe_run(["netsh", "advfirewall", "firewall", "show", "rule", "name=all"])
    info["firewall_state"] = safe_run(["netsh", "advfirewall", "show", "allprofiles"])
    info["netstat"] = safe_run(["netstat", "-ano"])
    info["shares"] = safe_run(["net", "share"])
    info["password_policy"] = safe_run(["net", "accounts"])
    info["routes"] = safe_run(["route", "print"])

    self.report["windows_info"] = info
