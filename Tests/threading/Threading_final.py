from concurrent.futures import ThreadPoolExecutor
import socket
def scan_ports(target_ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((target_ip, port)) == 0:
                print(f"Port {port} is open on {target_ip}.")
    except socket.error:
        print("There is a socket error")

def scan_ports_range(target_ip, start_port, end_port):
    with ThreadPoolExecutor(max_workers=20) as executor:
        port_range = range(start_port, end_port + 1)
        futures = [executor.submit(scan_ports, target_ip, port) for port in port_range]

        for future in futures:
            future.result()

target_ip = '192.168.1.4'
start_port = 0
end_port = 1000
scan_ports_range(target_ip, start_port, end_port)
