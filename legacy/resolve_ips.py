import socket

hosts = [
    "ac-8tkitlg-shard-00-00.ff23ewx.mongodb.net",
    "ac-8tkitlg-shard-00-01.ff23ewx.mongodb.net",
    "ac-8tkitlg-shard-00-02.ff23ewx.mongodb.net"
]

for host in hosts:
    try:
        ip = socket.gethostbyname(host)
        print(f"{host}: {ip}")
    except Exception as e:
        print(f"{host}: Error {e}")
