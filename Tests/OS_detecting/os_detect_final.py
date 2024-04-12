def detectOS():
    target='192.168.93.19'
    data = {'192.168.93.19': {'osmatch': [{'name': 'Microsoft Windows 10 1607', 'accuracy': '100', 'line': '69748', 'osclass': {'type': 'general purpose', 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': '10', 'accuracy': '100'}, 'cpe': 'cpe:/o:microsoft:windows_10:1607'}], 'ports': [{'protocol': 'tcp', 'portid': '80', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '128', 'service': {'name': 'http', 'method': 'table', 'conf': '3'}, 'cpe': [], 'scripts': []}, {'protocol': 'tcp', 'portid': '135', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '128', 'service': {'name': 'msrpc', 'method': 'table', 'conf': '3'}, 'cpe': [], 'scripts': []}, {'protocol': 'tcp', 'portid': '139', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '128', 'service': {'name': 'netbios-ssn', 'method': 'table', 'conf': '3'}, 'cpe': [], 'scripts': []}, {'protocol': 'tcp', 'portid': '443', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '128', 'service': {'name': 'https', 'method': 'table', 'conf': '3'}, 'cpe': [], 'scripts': []}, {'protocol': 'tcp', 'portid': '445', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '128', 'service': {'name': 'microsoft-ds', 'method': 'table', 'conf': '3'}, 'cpe': [], 'scripts': []}, {'protocol': 'tcp', 'portid': '902', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '128', 'service': {'name': 'iss-realsecure', 'method': 'table', 'conf': '3'}, 'cpe': [], 'scripts': []}, {'protocol': 'tcp', 'portid': '912', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '128', 'service': {'name': 'apex-mesh', 'method': 'table', 'conf': '3'}, 'cpe': [], 'scripts': []}, {'protocol': 'tcp', 'portid': '3306', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '128', 'service': {'name': 'mysql', 'method': 'table', 'conf': '3'}, 'cpe': [], 'scripts': []}], 'hostname': [], 'macaddress': None}, 'runtime': {'time': '1710003742', 'timestr': 'Sat Mar  9 22:32:22 2024', 'summary': 'Nmap done at Sat Mar  9 22:32:22 2024; 1 IP address (1 host up) scanned in 2.98 seconds', 'elapsed': '2.98', 'exit': 'success'}, 'stats': {'scanner': 'nmap', 'args': '"C:/Program Files (x86)/Nmap/nmap.exe" -v -oX - -O 192.168.93.19', 'start': '1710003740', 'startstr': 'Sat Mar  9 22:32:20 2024', 'version': '7.93', 'xmloutputversion': '1.05'}, 'task_results': [{'task': 'Parallel DNS resolution of 1 host.', 'time': '1710003740'}, {'task': 'SYN Stealth Scan', 'time': '1710003740', 'extrainfo': '1000 total ports'}]}


    os_info = data[target]['osmatch'][0]['name']
    os_type = data[target]['osmatch'][0]['osclass']['type']
    os_vendor = data[target]['osmatch'][0]['osclass']['vendor']
    os_family = data[target]['osmatch'][0]['osclass']['osfamily']

    print("OS Information:")
    print("Name:", os_info)
    print("Type:", os_type)
    print("Vendor:", os_vendor)
    print("Family:", os_family)

detectOS()
