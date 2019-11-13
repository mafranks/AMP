import xml.etree.ElementTree as ET

class Compare:

    def __init__(self):
        self.path1 = input("What is the full path of the first policy.xml?")
        self.path2 = input("what is the full path of the second policy.xml?")

    def parse_xml(self, path):
        """
        takes policy key's and their route-to-values, returns dictionary of the key-value pairs
        """

        policy_key = {
            "Business_UUID": ("Object", "config", "janus", "business", "uuid"), # business UUID in the AMP cloud
            "Policy_Serial_Number": ("Object", "config", "janus", "policy", "serial_number"), # policy serial number
            "Policy_UUID": ("Object", "config", "janus", "policy", "uuid"), # policy UUID in the AMP cloud
            "Policy_Name": ("Object", "config", "janus", "policy", "name"), # policy name
            "Identity_Sync_Enabled": ("Object", "config", "janus", "agent_guid_sync_type"), # Identity sync enabled?
            "Cache_TTL_Unknown_Files": ("Object", "config", "agent", "cloud", "cache", "ttl", "unknown"), # cached time to live for unknown hashes
            "Cache_TTL_Clean_Files": ("Object", "config", "agent", "cloud", "cache", "ttl", "clean"), # cached time to live for clean hashes
            "Cache_TTL_Malicious_Files": ("Object", "config", "agent", "cloud", "cache", "ttl", "malicious"), # cached time to live for malicious hashes
            "Cache_TTL_Unseen_Files": ("Object", "config", "agent", "cloud", "cache", "ttl", "unseen"), # cached time to live for unseen hashes
            "Cache_TTL_Blocked_Files": ("Object", "config", "agent", "cloud", "cache", "ttl", "block"), # cached time to live for blocked hashes
            "Quarantine_Action": ("Object", "config", "agent", "driver", "protmode", "qaction"), # qaction 0=audit, 1=quarantine
            "Monitor_File_Copy_Move": ("Object", "config", "agent", "driver", "protmode", "file"), # monitor file copy/move
            "Monitor_File_Executes": ("Object", "config", "agent", "driver", "protmode", "process"), # monitor file executes
            "System_Process_Protection_Enabled": ("Object", "config", "agent", "driver", "selfprotect", "spp"), # SPP enabled?
            "System_Process_Protection_Quarantine_Action": ("Object", "config", "agent", "driver", "selfprotect", "spp_qaction"), # SPP quarantine action
            "Exploit_Prevention_Enabled": ("Object", "config", "agent", "exprev", "enable"), # Exprev enabled?
            "ETHOS_Scan_On_Copy_Move": ("Object", "config", "agent", "scansettings", "ethos", "file"), # ETHOS on file copy/move
            "ETHOS_Enabled": ("Object", "config", "agent", "scansettings", "ethos", "enable"), # ETHOS enabled?
            "ETHOS_Max_Filesize": ("Object", "config", "agent", "scansettings", "ethos", "maxfilesize"), # ETHOS maximum filesize to be analyzed
            "Max_Archive_Filesize": ("Object", "config", "agent", "scansettings", "maxarchivefilesize"), # archive maximum filesize to be analyzed
            "Max_Filesize": ("Object", "config", "agent", "scansettings", "maxfilesize"), # maximum filesize to be analyzed
            "Scheduled_Scan_Enabled": ("Object", "config", "agent", "scansettings", "scheduled"), # scheduled scan set?
            "SPERO_Enabled": ("Object", "config", "agent", "scansettings", "spero", "enable"), # SPERO enabled?
            "TETRA_Scan_Archives": ("Object", "config", "agent", "scansettings", "tetra", "options", "ondemand", "scanarchives"), # Will TETRA scan archives?
            "TETRA_Deep_Scan": ("Object", "config", "agent", "scansettings", "tetra", "options", "ondemand", "deepscan"), # Will TETRA deep scan?
            "TETRA_Scan_Packed_Files": ("Object", "config", "agent", "scansettings", "tetra", "options", "ondemand", "scanpacked"), # Will TETRA scan packed files?
            "TETRA_Automatic_Update": ("Object", "config", "agent", "scansettings", "tetra", "updater", "enable"), # TETRA definitions automatically updating?
            "TETRA_Update_Server": ("Object", "config", "agent", "scansettings", "tetra", "updater", "server"), # TETRA update server settings
            "TETRA_Update_Interval": ("Object", "config", "agent", "scansettings", "tetra", "updater", "interval"), # TETRA update interval
            "TETRA_Enabled": ("Object", "config", "agent", "scansettings", "tetra", "enable"), # TETRA enabled?
            "URL_Scanner_Enabled": ("Object", "config", "agent", "urlscanner", "enable"), # URL Scanner enabled?  (Future feature, not currently functional)
            "Orbital_Enabled": ("Object", "config", "orbital", "enabled"), # Orbital enabled?  (Currently in beta)
            "Endpoint_Isolation_Enabled": ("Object", "config", "agent", "endpointisolation", "enable"), # Endpoint isolation enabled?
            "Connector_Protection_Enabled": ("Object", "config", "agent", "control", "serviceex"), # Connector protection enabled?
            "Uninstall_Password_Configured": ("Object", "config", "agent", "control", "uninstallex"), # Uninstall password configured?
            "Network_Monitoring_Quarantine_Action": ("Object", "config", "agent", "nfm", "settings", "qaction"), # Network monitoring quarantine action based on file hash, 0=Audit, 1=Blocking if hash is malicious
            "Network_Monitoring_Mode": ("Object", "config", "agent", "nfm", "settings", "mode"), # Network monitoring mode, 0=Audit, 1=Passive (allow until disposition received), 2=Active (block until disposition received)
            "Network_Monitoring_Enabled": ("Object", "config", "agent", "nfm", "enable"), # Network monitoring enabled?
            "Heartbeat_Interval": ("Object", "config", "agent", "hb", "interval"), # heartbeat interval to reach out to AMP cloud for updates
            "Agent_Log_Level": ("Object", "config", "agent", "log", "level"), # Default=0, Debug=7FFFFFFFFF
            "Command_Line_Logging_Enabled": ("Object", "config", "agent", "log", "showcmdline"), # Command line logging enabled?
            "Command_Line_Capture_Enabled": ("Object", "config", "agent", "cmdlinecapture", "enable"), # Command line capture enabled?
            "Verbose_History_Enabled": ("Object", "config", "agent", "history", "verbose"), # Verbose history enabled?
            "Update_Server_Address": ("Object", "config", "updater", "server"), # Update server address
            "Cloud_Notifications_Enabled": ("Object", "config", "ui", "notification", "cloud"), # Cloud notifications enabled in iptray
            "Hide_IOD_Toast": ("Object", "config", "ui", "notification", "hide_ioc_toast"), # Hide user notifications for IOCs?
            "Hide_File_Toast": ("Object", "config", "ui", "notification", "hide_file_toast"), # Hide user notifications for file convications?
            "Hide_Network_Monitoring_Toast": ("Object", "config", "ui", "notification", "hide_nfm_toast"), # Hide user notifications for network monitoring?
            "Hide_Exploit_Prevention_Toast": ("Object", "config", "ui", "notification", "hide_exprev_toast"), # Hide user notifications for Exploit Prevention?
            "Hide_User_Notifications_Toast": ("Object", "config", "ui", "notification", "hide_detection_toast"), # Hide user notifications for all engines?  (Controls all toast notifications after 6.2.1)
            "Tray_Log_Level": ("Object", "config", "ui", "log", "level"), # Tray log level, Default=0, Debug=17179869183
            "Connector_Log_Level": ("Object", "config", "monitor", "log", "level"), # Connector log level, Default = 0, Debug=1
            "Show_IP_Tray": ("Object", "config", "ui", "enable"), # Start IP Tray at startup?, 0=silent mode, 1=visible to users
            "Send_User_Info": ("Object", "config", "janus", "senduserinfo"), # Send username with events?
            "Proxy_Authentication_Type": ("Object", "config", "proxy", "authtype"), # Proxy authentication type
            "Proxy_Server_Address": ("Object", "config", "proxy", "server"), # Proxy address
            "Proxy_For_DNS": ("Object", "config", "proxy", "nolocalresolvehost"), # User proxy server for DNS?  (Only works for HTTP proxies)
            "Proxy_PAC_URL": ("Object", "config", "proxy", "pacloc"), # Proxy PAC file URL
            "Proxy_Password": ("Object", "config", "proxy", "password"), # Proxy password
            "Proxy_Port": ("Object", "config", "proxy", "port"), # Proxy port
            "Proxy_Type": ("Object", "config", "proxy", "type"), # Proxy server type
            "Proxy_Username": ("Object", "config", "proxy", "username") # Proxy username
        }

        policy_dict = {}
        
        root = self.get_root(path)
            
        policy_dict["Path_Exclusions"] = self.dig_thru_xml("Object", "config", "exclusions", "info", "item", root=root, is_list=True)
        policy_dict["Process_Exclusions"] = self.dig_thru_xml("Object", "config", "exclusions", "process", "item", root=root, is_list=True)        
        
        for i in policy_key.items():
            policy_dict[i[0]] = self.dig_thru_xml(*i[1], root=root)
        return policy_dict

    def get_root(self, path):
        with open(path) as f:
            tree = ET.parse(f)
            root = tree.getroot()
        return root

    
    def dig_thru_xml(self, *args, root, tag="{http://www.w3.org/2000/09/xmldsig#}", is_list=False):
        for arg in args[:-1]:
            query = f"{tag}{arg}"
            root = root.findall(query)
            if root:
                root = root[0]
            else:
                return None
        root = root.findall(f"{tag}{args[-1]}")
        if root:
            if is_list:
                return [i.text for i in root]
            else:
                return root[0].text
        return None

    def compare_policies(self):
        for key in self.policy_dict1.keys():
            if key == "Path_Exclusions":
                print("Path Exclusion Differences:\n")
                print("\nIn Policy1, but not in Policy2:\n")
                for value in self.policy_dict1.get(key):
                    if value not in self.policy_dict2.get(key):
                        print(f"{value.split('|')[-1]}")
                print("\n"+"*"*40+"\n")
                print("\nIn Policy2, but not in Policy1:\n")
                for value in self.policy_dict2.get(key):
                    if value not in self.policy_dict1.get(key):
                        print(f"{value.split('|')[-1]}")
                print("\n"+"*"*40+"\n")
            elif key == "Process_Exclusions":
                print("Process Exclusion Differences:\n")
                print("\nIn Policy1, but not in Policy2:\n")
                for value in self.policy_dict1.get(key):
                    #print(value)
                    if value not in self.policy_dict2.get(key):
                        print(f"{value.split('|')[-3]}")
                print("\n"+"*"*40+"\n")
                print("\nIn Policy2, but not in Policy1:\n")
                for value in self.policy_dict2.get(key):
                    if value not in self.policy_dict1.get(key):
                        print(f"{value.split('|')[-3]}")
                print("\n"+"*"*40+"\n")
            elif not self.policy_dict1.get(key) == self.policy_dict2.get(key):
               print(f"{key:20}: \nPolicy1: {self.policy_dict1.get(key)}\nPolicy2: {self.policy_dict2.get(key)}\n")

    
    def main(self):
        self.policy_dict1 = self.parse_xml(self.path1)
        self.policy_dict2 = self.parse_xml(self.path2)
        self.compare_policies()

a = Compare()
a.main()
