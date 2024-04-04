import nmap3

def get_os_info(target_ip):
    try:
        scanner = nmap3.Nmap()
        result = scanner.nmap_os_detection(target_ip)
        if target_ip in result and 'osmatch' in result[target_ip] and len(result[target_ip]['osmatch']) > 0:
            os_info = result[target_ip]['osmatch'][0]['name']
            os_type = result[target_ip]['osmatch'][0]['osclass']['type']
            os_vendor = result[target_ip]['osmatch'][0]['osclass']['vendor']
            os_family = result[target_ip]['osmatch'][0]['osclass']['osfamily']
            return os_info, os_type, os_vendor, os_family
        else:
            return None, None, None, None
    except Exception as e:
        print("An error occurred in OS detection:", e)
        return None, None, None, None

def get_service_info(target_ip, start_port, end_port):
    try:
        scanner = nmap3.Nmap()
        result = scanner.nmap_version_detection(target_ip, args=f"-p {start_port}-{end_port}")
        if target_ip in result and 'ports' in result[target_ip] and len(result[target_ip]['ports']) > 0:
            services = []
            for port in result[target_ip]['ports']:
                if port['state'] == 'open':  # Check if the port is open (service is running)
                    service_name = port['service']['name']
                    service_version = port['service'].get('version', 'unknown')
                    if service_version != 'unknown':
                        services.append(f"Port {port['portid']} | Service: {service_name} | Version: {service_version}")
                    else:
                        services.append(f"Port {port['portid']} | Service: {service_name}")
            if services:
                for service in services:
                    print(service)
            else:
                return ["No open ports found."]
        else:
            return ["No open ports found."]
    except nmap3.NmapExecutionException as e:
        print("An error occurred in service detection:", e)
        return ["An error occurred in service detection."]
