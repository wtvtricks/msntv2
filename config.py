import requests 

# Server config
ip = 'Automatic' 
server_ip = ''
home_port = 7070
headwaiter_port = 6060
sg_port = 80
upstream_dns = '1.0.0.1'

# Automatically get the server IP if specified
if ip.lower() == "automatic":
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Raise an error for bad responses
        ip_data = response.json()
        server_ip = ip_data['ip']
        print(f"Successfully got IP: {server_ip}")
    except requests.RequestException as e:
        print(f"Error retrieving IP: {e}")
        print("Make sure you have an internet connection or that api.ipify.org isn't blocked.")
        exit()
else:
    print(f"Using manual configuration for server IP: {server_ip}")


if not server_ip:
    print("Server IP is not set. Please configure it manually in the config file.")
    exit()
