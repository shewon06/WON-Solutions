import socket

hosts = [
    "ac-8tkitlg-shard-00-00.ff23ewx.mongodb.net",
    "ac-8tkitlg-shard-00-01.ff23ewx.mongodb.net",
    "ac-8tkitlg-shard-00-02.ff23ewx.mongodb.net"
]

ips = []
for host in hosts:
    try:
        ip = socket.gethostbyname(host)
        ips.append(f"{ip}:27017")
    except:
        pass

conn_str = f"mongodb://Vercel-Admin-atlas-amber-gardenc:XGrObDyQBHhk9TN5@{','.join(ips)}/?replicaSet=atlas-amber-gardenc-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority"
print(conn_str)
with open("conn_str.txt", "w") as f:
    f.write(conn_str)
