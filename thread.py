import threading
import serve
import dns
import config

def run_home():
    serve.home.run(host=config.server_ip, port=config.home_port, threaded=True)

def run_headwaiter():
    serve.headwaiter.run(host=config.server_ip, port=config.headwaiter_port, threaded=True)

def run_service():
    serve.service.run(host=config.server_ip, port=config.sg_port, threaded=True)

def run_dns_server():
    resolver = dns.RedirectResolver()
    server = dns.DNSServer(resolver, port=53, address=config.server_ip, tcp=False)
    server.start()

def run():
    home_thread = threading.Thread(target=run_home)
    bootstrap_thread = threading.Thread(target=run_headwaiter)
    service_thread = threading.Thread(target=run_service)
    dns_thread = threading.Thread(target=run_dns_server)
    # Start all threads
    home_thread.start()
    bootstrap_thread.start()
    service_thread.start()
    dns_thread.start()
    print("Started Home service")
    print("Started Bootstrap service")
    print("Started SG service")
    print("Started DNS service")
    home_thread.join()
    bootstrap_thread.join()
    service_thread.join()
    dns_thread.join()