from dnslib import DNSRecord, QTYPE, RR, A, DNSHeader
import socket
import socketserver

# GET the local IP address (and print it)
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"You have IP: {local_ip}")

# DNS server config (mapping domain names to the local machine's ip)
DOMAIN_TO_IP = {
    'a.com.': local_ip,
    'b.com.': local_ip 
}

class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip() # reads the incoming data
        socket = self.request[1] 
        try:
            request = DNSRecord.parse(data) # parses the DNS request
            qname = str(request.q.qname)
            qtype = QTYPE[request.q.qtype]

            print(f"Received request for: {str(qname)}")

            # Creating DNS response
            # DNS reply format HEADER: id = same id as request id + qr=1 for response + aa=1 to let know the info is from original source (not cache)
            # + ra=1 for recursive access (can contact other DNS server)
            # q is given so the reply has same question section as the request.
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

            if qname in DOMAIN_TO_IP:
                # adds answer section to dns reply
                reply.add_answer(RR(qname, QTYPE.A, rdata=A(DOMAIN_TO_IP[qname])))
                print(f"Resolved {qname} to {DOMAIN_TO_IP[qname]}")
            else:
                print(f"No record found for {qname}")
            
            socket.sendto(reply.pack(), self.client_address)
        except Exception as e:
            print(f"error handling request: {e}")

if __name__ == "__main__":
    server = socketserver.UDPServer(("0.0.0.0", 53), DNSHandler)
    print("DNS server is running...")
    server.serve_forever()