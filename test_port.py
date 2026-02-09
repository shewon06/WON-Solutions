import socket

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is OPEN on {host}")
        else:
            print(f"Port {port} is CLOSED on {host} (Error code: {result})")
    except Exception as e:
        print(f"Error checking {host}:{port} -> {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    check_port("195.201.179.80", 3306)
    check_port("won.systems", 3306)
    check_port("www.won.systems", 3306)
