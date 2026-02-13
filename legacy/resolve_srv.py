import dns.resolver

srv_record = "_mongodb._tcp.atlas-amber-gardenc.ff23ewx.mongodb.net"

try:
    answers = dns.resolver.resolve(srv_record, 'SRV')
    for rdata in answers:
        print(f"Host: {rdata.target}, Port: {rdata.port}")
except Exception as e:
    print(f"Error: {e}")
