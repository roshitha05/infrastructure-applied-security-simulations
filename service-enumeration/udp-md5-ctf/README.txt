# UDP Service Enumeration & MD5 Hash Cracking (CTF Simulation)

This module documents the process of identifying a hidden UDP service and recovering a voucher code generated using MD5.

The scenario:
A server generates voucher codes using:

VoucherCode = MD5(A || ClientID || B)

Where:
- A = two lowercase letters
- ClientID = 7-digit student ID
- B = two symbols

The objective was to:
1) Identify the running service and port
2) Retrieve a voucher hash
3) Recover the plaintext using Crunch + Hashcat

------------------------------------------------------------
Step 1 – Running the Server (Ubuntu VM)
------------------------------------------------------------

The provided executable server was made executable:

chmod +x executable_server

Then started on the Ubuntu VM:

./executable_server

The service runs using UDP on an unknown port between 12345–12500.

------------------------------------------------------------
Step 2 – Service Discovery (Kali VM)
------------------------------------------------------------

Initial TCP scan showed no open ports.

Since the assignment specified UDP, a UDP scan was performed:

nmap -sU <ubuntu_ip>

The scan revealed the service running on UDP port 12433.

------------------------------------------------------------
Step 3 – Retrieving the Voucher Code
------------------------------------------------------------

Since the service uses UDP, netcat was used with UDP mode:

nc -u <ubuntu_ip> 12433

The ClientID (UOW student ID) was sent to the server.

The server returned the voucher hash:

497685f5c1fbe8d61640a2470bd0ceaa

------------------------------------------------------------
Step 4 – Wordlist Generation (Crunch)
------------------------------------------------------------

The known format:

A (2 lowercase letters)
ClientID (7 digits)
B (2 symbols)

Total length:
2 + 7 + 2 = 11 characters

Crunch was used to generate all combinations:

crunch 11 11 -t @@8768511,^^

Where:
@ = lowercase letters
^ = symbols

This generated the required wordlist.

------------------------------------------------------------
Step 5 – Preparing the Hash File
------------------------------------------------------------

Initially encountered "Token length exception" in Hashcat due to formatting.

Fixed by creating a clean hash file:

echo -n 497685f5c1fbe8d61640a2470bd0ceaa > hash.txt

Ensured it was exactly 32 characters (valid MD5 length).

------------------------------------------------------------
Step 6 – Cracking the Hash (Hashcat)
------------------------------------------------------------

hashcat -m 0 -a 0 hash.txt wordlist.txt

Where:
- -m 0   = MD5 hash type
- -a 0   = dictionary attack
- hash.txt = target hash
- wordlist.txt = Crunch output

Hashcat successfully cracked the hash.

------------------------------------------------------------
Final Results
------------------------------------------------------------

Voucher Hash:
497685f5c1fbe8d61640a2470bd0ceaa

Recovered Plaintext:
kg8768511,(

Prefix (A):
kg

Suffix (B):
,(

------------------------------------------------------------
What This Demonstrates
------------------------------------------------------------

- UDP service discovery
- Understanding of hash formats
- Structured wordlist generation
- Dictionary attack using Hashcat
- Weakness of MD5 for security-sensitive operations

------------------------------------------------------------
Security Relevance
------------------------------------------------------------

This highlights why:

- MD5 should never be used for security-critical systems
- Services should not expose predictable hash-based tokens
- Proper salting and strong hashing (e.g., SHA-256 + salt) is necessary
- UDP services should not be left exposed without proper filtering

------------------------------------------------------------
Note
------------------------------------------------------------

Performed strictly in a controlled lab environment.