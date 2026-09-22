# ARP Spoofing (Lab Simulation)

This script performs a basic ARP spoofing attack using Python and Scapy.

The goal is simple:
Trick the victim into thinking the attacker (Kali) is the gateway.

Once poisoned, traffic meant for the gateway is redirected to the attacker.

Built and tested in a controlled VirtualBox lab (Kali + Metasploitable2).

------------------------------------------------------------
How It Works
------------------------------------------------------------

- Uses Scapy to craft ARP reply packets (op=2).
- Sends forged ARP responses to:
    1) Victim → pretending to be the gateway
    2) Gateway → pretending to be the victim
- Repeats every 2 seconds to maintain poisoning.
- Stops cleanly when Ctrl+C is pressed.

The script dynamically retrieves the target’s MAC address before spoofing.

------------------------------------------------------------
Requirements
------------------------------------------------------------

- Python 3
- Scapy installed
- Root privileges (raw packet sending)
- Both machines on same network

Check Scapy:
python3 -c "import scapy"

Enable IP forwarding (important if doing MITM properly):
sudo sysctl -w net.ipv4.ip_forward=1

------------------------------------------------------------
How To Run (Lab Only)
------------------------------------------------------------

Step 1 – Find your gateway IP:

ip route | grep default

You should see something like:
default via 10.0.2.1 dev eth0

Step 2 – Run the script:

sudo python3 arpspoof.py <victim_ip> <gateway_ip>

Example (Metasploitable2 victim):

sudo python3 arpspoof.py 10.0.2.4 10.0.2.1

------------------------------------------------------------
Expected Output
------------------------------------------------------------

Author: Roshitha
Date: 19/02/2026

[*] Using interface: eth0
[*] Got MAC address for 10.0.2.4
[*] Victim MAC retrieved
[*] Starting ARP poison – press Ctrl-C to stop

When you press Ctrl+C:

[!] Caught SIGINT – restoring victim's ARP entry
[*] Restored original ARP entry

------------------------------------------------------------
What This Demonstrates
------------------------------------------------------------

- ARP cache poisoning
- Man-in-the-middle setup
- Layer 2 trust weakness
- How local network attacks work

ARP has no authentication, so devices trust unsolicited replies.
That is the core weakness being exploited here.

------------------------------------------------------------
Defensive Relevance
------------------------------------------------------------

This highlights why:

- Static ARP entries can help in critical systems
- Network segmentation matters
- Monitoring abnormal ARP traffic is important
- ARP inspection (DAI) should be enabled in managed switches

------------------------------------------------------------
Note
------------------------------------------------------------

Strictly for educational use in isolated lab environments.
Do not run on networks you do not own or have permission to test.