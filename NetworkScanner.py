import socket
import re
import ipaddress
from concurrent.futures import ThreadPoolExecutor
# If Detection module is in the same directory, you can import it directly
from Detection import get_service_info, get_os_info

# For checking if the IP is valid
ip_add_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

# For checking if the port range is valid
port_range_pattern = re.compile(r"(\d+)-(\d+)")

port_min = 0
port_max = 1024  # Program is capped at 1024 ports for now

# Function to validate IP address
def is_valid_ip(ip):
    return bool(ip_add_pattern.match(ip))

# Function to scan ports concurrently
def scan_ports(target_ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((target_ip, port)) == 0:
                return port
    except socket.timeout:
        return f"Timeout while connecting to {target_ip}:{port}"
    except ConnectionRefusedError:
        return f"Connection refused on port {port} for {target_ip}"
    except ConnectionResetError:
        return f"Connection reset on port {port} for {target_ip}"
    except Exception as e:
        return f"An error occurred: {e}"

def scan_ports_range(target_ip, start_port, end_port):
    open_ports = []  # List to store open ports
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        port_range = range(start_port, end_port + 1)
        futures = [executor.submit(scan_ports, target_ip, port) for port in port_range]
        
        for future in futures:
            result = future.result()
            if isinstance(result, int):
                open_ports.append(result)
            elif result is not None:
                print(result)
    
    if open_ports:
        print(f"Open ports on {target_ip}: {', '.join(map(str, open_ports))}")
        return open_ports
    else:
        pass
        print(f"No open ports found on {target_ip}")

# For getting the target to scan (Both scans)
def get_scan_target():
    while True:
        choice = input("\nDo you want to scan a network (N) or a single device (S)? ").strip().upper()
        while choice not in ['N', 'S']:
            choice = input("⚠ Wrong Entry !! Please enter 'N' for network scanning or 'S' for single device scanning: ").strip().upper()
        print("⚠ Os_detection requiers Admin privileges")
        os_detection_switch = input("Do you want to run OS detection (Y/N): ").strip().upper()
        while os_detection_switch not in ['Y', 'N']:
            os_detection_switch = input("⚠ Wrong Entry!! Please enter 'Y' or 'N' for OS detection: ").strip().upper()
        if choice == 'N':
            if os_detection_switch == 'Y':
                return get_network(), True
            else:
                return get_network(), False
        elif choice == 'S':
            if os_detection_switch == 'Y':
                return get_single_device(), True
            else:
                return get_single_device(), False
        else:
            print("Invalid choice. Please enter 'N' for network scanning or 'S' for single device scanning.")

# Function to get a network address for scanning
def get_network():
    while True:
        network_ip = input("Please enter the IP network address that you want to scan (e.g., 192.168.0.0/24): ")
        try:
            network = ipaddress.ip_network(network_ip, strict=False)
            if network.num_addresses > 1:  # Ensure it's a network, not a single IP
                print(f"{network} is a valid IP network address")
                return network
            else:
                print("Please enter a valid IP network address with multiple hosts.")
        except ValueError:
            print("Invalid IP network address. Please try again.")

# Function to get a single device IP address for scanning
def get_single_device():
    while True:
        ip_device_entered = input("Please enter the IP address of the device that you want to scan (e.g., 192.168.0.0): ")
        if is_valid_ip(ip_device_entered):
            print(f"{ip_device_entered} is a valid IP address")
            return ip_device_entered
        else:
            print("Invalid IP address. Please try again.")

# Function to get the port range for scanning
def get_port_range():
    global port_min, port_max
    while True:
        print("Please enter the range of ports you want to scan in format: <int>-<int> (e.g., 60-120)")
        port_range = input("Enter port range: ")
        port_range_valid = port_range_pattern.search(port_range.replace(" ", ""))
        if port_range_valid:
            port_min = int(port_range_valid.group(1))
            port_max = int(port_range_valid.group(2))
            return port_min, port_max
        else:
            print("Invalid port range format. Please try again.")

# Main function for scanning
def main():
    scan, os_detection = get_scan_target()
    start_port, end_port = get_port_range()

    # Service detection switch
    service_Detection = input("Do you want to detect services (Y/N): ").strip().upper()
    while service_Detection not in ['Y', 'N']:
        service_Detection = input("⚠ Wrong Entry!! Please enter 'Y' or 'N' for service detection: ").strip().upper()
    if service_Detection == 'Y':
        service_switch = True
    else:
        service_switch = False

    if isinstance(scan, ipaddress.IPv4Network):
        for ip_address in scan.hosts():
            Scanning = scan_ports_range(str(ip_address), start_port, end_port)
            # Calling os-detection module for network scan
            if service_switch:
                get_service_info(str(ip_address), start_port, end_port)
            if os_detection and Scanning:
                os_info, os_type, os_vendor, os_family = get_os_info(scan)
                print(f"OS Info: {os_info}")
                print(f"OS Type: {os_type}")
                print(f"OS Vendor: {os_vendor}")
                print(f"OS Family: {os_family}")
                
    elif is_valid_ip(scan):
        scan_ports_range(scan, start_port, end_port)
        # calling os-detection module for single device scan
        if service_switch:
            get_service_info(scan, start_port, end_port)
        if os_detection:
            os_info, os_type, os_vendor, os_family = get_os_info(scan)
            print(f"OS Info: {os_info}")
            print(f"OS Type: {os_type}")
            print(f"OS Vendor: {os_vendor}")
            print(f"OS Family: {os_family}")
    else:
        print("Invalid target for scanning.")


# Call the main function
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
