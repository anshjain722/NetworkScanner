import socket
import threading

def test(ip, start_port, end_port):
    try:
        def scan_port(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result = s.connect_ex((ip, port))
                if result == 0:
                    service_name = socket.getservbyport(port)
                    print(f"Port {port} ({service_name}) on {ip} is open")
                s.close()
            except Exception as e:
                print(f"An error occurred while scanning port {port}: {e}")

        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=scan_port, args=(port,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
target_ip = "127.0.0.1"
start_port = 1
end_port = 3000

test(target_ip, start_port, end_port)
