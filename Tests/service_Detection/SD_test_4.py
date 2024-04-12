import nmap3

target = '127.0.0.1'
nmap = nmap3.Nmap()

# Perform Nmap scan to identify running services on each port
results = nmap.nmap_version_detection(target)

# Extract and print service information
print("Services running on ports:")
for port_info in results[target]['ports']:
    port = port_info['portid']
    state = port_info['state']
    service_name = port_info['service']['name']
    product = port_info['service'].get('product', 'Unknown')
    version = port_info['service'].get('version', 'Unknown')
    extrainfo = port_info['service'].get('extrainfo', '')
    
    print(f"Port {port} ({state}): {service_name} - {product} {version} ({extrainfo})")
