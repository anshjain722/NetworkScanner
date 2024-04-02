import socket
import re
import ipaddress
from concurrent.futures import ThreadPoolExecutor

# For checing if the IP is valid
ip_add_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

# For checking if the port range is valid
port_range_pattern = re.compile(r"(\d+)-(\d+)")

port_min = 0
port_max = 1000 # Prgram is capped at 1000 ports for now

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
    else:
        #Not imp for normal use
        #print(f"No open ports found on {target_ip}")
        pass

# For getting the target to scan (Both scans)
def get_scan_target():
    while True:
        choice = input("\nDo you want to scan a network (N) or a single device (S)? ").strip().upper()
        if choice == 'N':
            return get_network()
        elif choice == 'S':
            return get_single_device()
        else:
            print("Invalid choice. Please enter 'N' for network scanning or 'S' for single device scanning.")

# Function to get a network address for scanning
def get_network():
    while True:
        ip_network_entered = input("Please enter the IP network address that you want to scan (e.g., 192.168.0.0/24): ")
        try:
            network = ipaddress.ip_network(ip_network_entered, strict=False)
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
        ip_device_entered = input("Please enter the IP address of the device that you want to scan: ")
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
        port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
        if port_range_valid:
            port_min = int(port_range_valid.group(1))
            port_max = int(port_range_valid.group(2))
            return port_min, port_max
        else:
            print("Invalid port range format. Please try again.")

# Main function for scanning
def main():
    target = get_scan_target()
    start_port, end_port = get_port_range()
    if isinstance(target, ipaddress.IPv4Network):
        for ip_address in target.hosts():
            scan_ports_range(str(ip_address), start_port, end_port)
    elif is_valid_ip(target):
        scan_ports_range(target, start_port, end_port)
    else:
        print("Invalid target for scanning.")

# Call the main function
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
