import socket
import re
import ipaddress
import concurrent.futures

ip_add_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
port_min = 0
port_max = 65535

open_ports = []

# Function to scan
def scan(ip_address, ports):
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((ip_address, port)) == 0:
                    open_ports.append((ip_address, port))
        except socket.error:
            print("There is a socket error")

# Function to validate IP address
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Function for deciding what to do
while True:
    choice = input("\nDo you want to scan a network (N) or a single device (S)? ").strip().upper()
    if choice == 'N':
        while True:
            ip_network_entered = input("Please enter the IP network address that you want to scan (e.g., 192.168.0.0/24): ")
            try:
                network = ipaddress.ip_network(ip_network_entered, strict=False)
                print(f"{network} is a valid IP network address")
                break
            except ValueError:
                print("Invalid IP network address. Please try again.")
        break
    elif choice == 'S':
        ip_device_entered = input("Please enter the IP address of the device that you want to scan: ")
        if ip_add_pattern.match(ip_device_entered):
            print(f"{ip_device_entered} is a valid IP address")
            break
        else:
            print("Invalid IP address. Please try again.")
    else:
        print("Invalid choice. Please enter 'N' for network scanning or 'S' for single device scanning.")

# Asking for port range from user
while True:
    print("Please enter the range of ports you want to scan in format: <int>-<int> (e.g., 60-120)")
    port_range = input("Enter port range: ")
    port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
    if port_range_valid:
        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        break

# function for scanning
if choice == 'N':
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = []
        for ip_address in network.hosts():
            ports = range(port_min, port_max + 1)
            results.append(executor.submit(scan, str(ip_address), ports))
        concurrent.futures.wait(results)
elif choice == 'S':
    ports = range(port_min, port_max + 1)
    scan(ip_device_entered, ports)

# Printing results
if open_ports:
    print("\nScan completed. Open ports found:")
    for ip, port in open_ports:
        print(f"Port {port} is open on {ip}.")
else:
    print("No open ports found.")
