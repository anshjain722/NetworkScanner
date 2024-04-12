import pprint
import nmap3
def detect_os(ip, port_range):
    try:
        nmap = nmap3.Nmap()
        os_info = nmap.nmap_os_detection(ip, args=f'-p{",".join(map(str, port_range))}')
        pprint.pprint(os_info)
        if os_info:
            print("OS Info Found")
            for ip, details in os_info.items():
                if 'osmatch' in details and isinstance(details['osmatch'], list):
                    os_match = details['osmatch']
                    if os_match:
                        os_class = os_match[0]['osclass']
                        if os_class:
                            os_family = os_class[0]['osfamily']
                            return os_family
            return "OS detection failed: No info!"
        else:
            return "OS detection failed: No response!"
    except Exception as e:
        if str(e) == 'You must be root/administrator to continue!':
            return "OS detection failed: You must be root/administrator to continue!"
        else:
            return f"OS detection failed: {str(e)}"

ip = 
detect_os()