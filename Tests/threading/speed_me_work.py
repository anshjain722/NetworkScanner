import socket
import re
import ipaddress
import threading

ip_add_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
port_min = 0
port_max = 65535

open_ports = []

# Function to scan ports
def scan_ports(ip_address, ports):
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

# Function for single device scan
def single_device_scan(ip_device_entered, port_min, port_max):
    if is_valid_ip(ip_device_entered):
        ports = range(port_min, port_max + 1)
        threading.Thread(target=scan_ports, args=(ip_device_entered, ports)).start()
    else:
        print("Invalid IP address. Please try again.")

# Function for network scan
def network_scan(ip_network_entered, port_min, port_max):
    try:
        network = ipaddress.ip_network(ip_network_entered, strict=False)
        for ip_address in network.hosts():
            ports = range(port_min, port_max + 1)
            threading.Thread(target=scan_ports, args=(str(ip_address), ports)).start()
    except ValueError:
        print("Invalid IP network address. Please try again.")

# Function for deciding what to do
while True:
    choice = input("\nDo you want to scan a network (N) or a single device (S)? ").strip().upper()
    if choice == 'N':
        while True:
            ip_network_entered = input("Please enter the IP network address that you want to scan (e.g., 192.168.0.0/24): ")
            network_scan(ip_network_entered, port_min, port_max)
            break
    elif choice == 'S':
        ip_device_entered = input("Please enter the IP address of the device that you want to scan: ")
        single_device_scan(ip_device_entered, port_min, port_max)
        break
    else:
        print("Invalid choice. Please enter 'N' for network scanning or 'S' for single device scanning.")

# Printing results
if open_ports:
    print("\nScan completed. Open ports found:")
    for ip, port in open_ports:
        print(f"Port {port} is open on {ip}.")
else:
    print("No open ports found.")
