from flask import Flask, render_template, send_from_directory, abort, request
import os
import logging
import threading
import time
from dnslib import DNSRecord, QTYPE, RR, A
from dnslib.server import DNSServer, BaseResolver
import socket

# Initialize Flask applications
bootstrap = Flask(__name__)
service = Flask(__name__)
home = Flask(__name__)

@bootstrap.route('/')
def returnBootstrap():
    return render_template("bootstrap.html")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

home_directory = os.path.join(os.getcwd(), 'Home')
home_directory2 = os.path.join(os.getcwd(), 'Home2')
images_shared_directory = os.path.join(home_directory2, 'Images', 'Shared')

@home.route('/Pages/<path:filename>')
def serve_file(filename):
    try:
        logging.debug(f"Trying to serve file from Home: {filename}")
        return send_from_directory(home_directory, filename)
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        abort(404)

@home.route('/Images/Shared/<path:filename>')
def serve_image(filename):
    try:
        logging.debug(f"Trying to serve image from Images/Shared: {filename}")
        return send_from_directory(images_shared_directory, filename)
    except FileNotFoundError:
        logging.error(f"Image not found: {filename}")
        abort(404)

@service.route('/')
def returnNilIfNoHTML():
    return render_template('eval.html')

@service.route('/connection/bootstrap.html', methods=['POST', 'GET'])
def strap():
    return render_template('bootstrap.html')

@service.route('/connection/boxcheck.html', methods=['POST', 'GET'])
def returnboxcheck():
    return render_template("boxcheck.html")

@service.route('/connection/usercheck.html')
def returnusercheck():
    return render_template("usercheck_mock.html")

@service.route('/connection/kickstart.aspx')
def returnkickstart():
    return render_template('kickstart.aspx')

@service.route('/connection/GatePage.aspx', methods=['GET'])
def gate_page():
    if request.args.get('phase') == 'Bootstrap' and request.args.get('purpose') == 'Authorize':
        return render_template('/connection/GatePage.aspx')
    else:
        return render_template('/connection/GatePage.aspx')

def run_home():
    home.run(host='0.0.0.0', port=7070)

def run_bootstrap():
    bootstrap.run(host='0.0.0.0', port=6060)

def run_service():
    service.run(host='0.0.0.0', port=80)

# DNS server code
REDIRECTS = {
    'example.com.': {'ip': '123.123.123.123', 'port': 80},
    'anotherdomain.com.': {'ip': '124.124.124.124', 'port': 8080},
    'headwaiter.trusted.msntv.msn.com.': {'ip': '172.234.28.223', 'port': 6060},
    'sg4.trusted.msntv.msn.com.': {'ip': '172.234.28.223', 'port': 80},
    'sg3.trusted.msntv.msn.com.': {'ip': '172.234.28.223', 'port': 80},
    'sg2.trusted.msntv.msn.com.': {'ip': '172.234.28.223', 'port': 80},
    'sg1.trusted.msntv.msn.com.': {'ip': '172.234.28.223', 'port': 80},
    'msntv.msn.com.': {'ip': '172.234.28.223', 'port': 7070},
    'login.live.com.': {'ip': '172.234.28.223', 'port': 1863},
    'login.live.com.lan.': {'ip': '172.234.28.223', 'port': 1863},
    'mail.services.live.com.': {'ip': '172.234.28.223', 'port': 1863},
}

WHITELIST = [
    '1.1.1.1'
]

log_file_path = os.path.join(os.path.dirname(__file__), 'dns-requests.log')

def log_request(query, rinfo, redirected=False, denied=False):
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    log_entry = f"{timestamp} - Query: {query.qname}, Type: {QTYPE[query.qtype]}, From: {rinfo[0]}, Redirected: {redirected}, Denied: {denied}\n"
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)
    print(log_entry.strip())

class ProxyResolver(BaseResolver):
    def resolve(self, request, handler):
        query = request.questions[0]
        qname = str(query.qname)
        qtype = QTYPE[query.qtype]
        rinfo = handler.client_address

        if rinfo[0] not in WHITELIST:
            log_request(query, rinfo, denied=True)
            print(f"Denied request from non-whitelisted IP: {rinfo[0]}")
            return request.reply()

        log_request(query, rinfo)

        if qname in REDIRECTS:
            log_request(query, rinfo, redirected=True)
            reply = request.reply()
            reply.add_answer(RR(
                qname,
                QTYPE.A,
                rdata=A(REDIRECTS[qname]['ip']),
                ttl=300
            ))
            return reply
        else:
            try:
                # Forward request to another DNS server
                upstream_server = ('8.8.8.8', 53)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(request.pack(), upstream_server)
                data, _ = sock.recvfrom(4096)
                sock.close()
                return DNSRecord.parse(data)
            except Exception as e:
                print(f"Failed to resolve DNS for {qname}: {e}")
                return request.reply()

def run_dns_server():
    resolver = ProxyResolver()
    server = DNSServer(resolver, port=53, address='0.0.0.0')
    print("DNS server listening on 0.0.0.0:53")
    server.start_thread()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()

if __name__ == '__main__':
    if not os.path.exists(home_directory):
        os.makedirs(home_directory)

    if not os.path.exists(images_shared_directory):
        os.makedirs(images_shared_directory)

    # Create threads for each Flask app and DNS server
    home_thread = threading.Thread(target=run_home)
    bootstrap_thread = threading.Thread(target=run_bootstrap)
    service_thread = threading.Thread(target=run_service)
    dns_thread = threading.Thread(target=run_dns_server)

    # Start the threads
    home_thread.start()
    bootstrap_thread.start()
    service_thread.start()
    dns_thread.start()

    # Wait for the threads to complete
    home_thread.join()
    bootstrap_thread.join()
    service_thread.join()
    dns_thread.join()
