import config
from dnslib import DNSRecord, QTYPE, RR, A
from dnslib.server import DNSServer, DNSHandler, BaseResolver
import socket
import logging

REDIRECTS = {
    'headwaiter.trusted.msntv.msn.com.': {'ip': config.server_ip, 'port': config.headwaiter_port},
    'sg4.trusted.msntv.msn.com.': {'ip': config.server_ip, 'port': config.sg_port},
    'sg3.trusted.msntv.msn.com.': {'ip': config.server_ip, 'port': config.sg_port},
    'sg2.trusted.msntv.msn.com.': {'ip': config.server_ip, 'port': config.sg_port},
    'sg1.trusted.msntv.msn.com.': {'ip': config.server_ip, 'port': config.sg_port},
    'msntv.msn.com.': {'ip': config.server_ip, 'port': config.home_port},
}

logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger()

# Function to validate an IP address
def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

class RedirectResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]

        if qname in REDIRECTS and qtype == 'A':
            redirect_info = REDIRECTS[qname]
            ip = redirect_info['ip']

            # Log the request and IP address being resolved
            logger.info(f"Request for {qname} from {handler.client_address}. IP resolved: {ip}")

            if is_valid_ip(ip):
                reply = request.reply()
                reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip), ttl=60))
                return reply
            else:
                logger.warning(f"Invalid IP address for {qname}: {ip}")
                reply = request.reply()
                reply.header.rcode = 3  # NXDOMAIN
                return reply
        else:
            # If the domain is not in the redirects, forward the request to 1.0.0.1
            logger.info(f"Query for unknown domain: {qname}. Forwarding the request to 1.0.0.1.")
            return self.forward_request(request)

    def forward_request(self, request):
        try:
            query = DNSRecord.question(str(request.q.qname), QTYPE.A)
            response = query.send(config.upstream_dns, 53)  # UDP port 53
            reply = DNSRecord.parse(response)
            reply.header.id = request.header.id
            reply.header.rcode = 0
            for answer in reply.rr:
                if isinstance(answer.rdata, A):
                    continue 
                else:
                    logger.warning(f"Unexpected record type for {reply.q.qname}: {answer.rdata}")

            return reply

        except Exception as e:
            logger.error(f"Error forwarding request for {request.q.qname}: {e}")
            reply = request.reply()
            reply.header.rcode = 3  # NXDOMAIN
            return reply
