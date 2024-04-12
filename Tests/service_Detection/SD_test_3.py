from nmap3 import Nmap
import json

def filter_json_data(data, keys_to_display):
    filtered_data = [{key: item[key] for key in keys_to_display if key in item} for item in data]
    return filtered_data

def service_detection(ip, start_port, end_port):
    nmap = Nmap()
    result = nmap.scan_top_ports(ip, args=f"-p {start_port}-{end_port}")

    for host, scan_result in result.items():
        print(f"Host: {host}")
        for proto, ports in scan_result.items():
            print(f"Protocol: {proto}")
            if proto == 'osmatch':
                filtered_os = filter_json_data(ports, ['osmatch'])
                print(filtered_os)
            elif proto == 'ports':
                filtered_ports = filter_json_data(ports, ['portid', 'service'])
                for port_info in filtered_ports:
                    port = port_info['portid']
                    service = port_info['service']['name']
                    print(f"Port: {port}\tService: {service}")
            else:
                print("Unknown protocol")

# Example usage
target_ip = "127.0.0.1"
start_port = 1
end_port = 3000

service_detection(target_ip, start_port, end_port)
