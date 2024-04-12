import socket
import threading
# code which detects http services running on the target machine
def test(ip, start_port, end_port):
    try:
        def detect_apache(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((ip, port))
                s.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
                response = s.recv(1024).decode()
                if "Server: Apache" in response:
                    print(f"Port {port} on {ip} is open: Apache HTTP Server")
                s.close()
            except:
                pass 

        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=detect_apache, args=(port,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    except:
        pass  # Suppress printing errors

# Example usage
target_ip = "127.0.0.1"
start_port = 1
end_port = 1000

test(target_ip, start_port, end_port)
