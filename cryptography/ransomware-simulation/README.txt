# Ransomware Simulation (Lab Only)

This script simulates basic ransomware behaviour using Python and OpenSSL.

The flow is simple:

1. Generate a random 16-byte symmetric key.
2. Generate an RSA key pair (attacker side).
3. Encrypt my_secrets.txt using AES-256-CBC.
4. Encrypt the symmetric key using the attacker’s public RSA key.
5. Delete the original secret file and plaintext key.
6. Display a ransom note.

Everything is done in a controlled Kali Linux lab environment.

------------------------------------------------------------
What This Script Actually Does
------------------------------------------------------------

- Uses `openssl rand -base64 16` to generate a 128-bit key.
- Uses AES-256-CBC to encrypt the victim file.
- Uses RSA (2048-bit) to encrypt the symmetric key.
- Base64-encodes ciphertext outputs so they are human readable.
- Deletes key.txt and my_secrets.txt after encryption.

This models hybrid encryption used in real ransomware:
Symmetric encryption for speed.
Asymmetric encryption for key protection.

------------------------------------------------------------
Required Files
------------------------------------------------------------

- ransomware.py
- my_secrets.txt  (must exist before running)

Example content of my_secrets.txt:

echo "This is a secret message – you will have to pay to get it back."

------------------------------------------------------------
How To Run (Lab Only)
------------------------------------------------------------

Step 1 – Go to the folder:

cd /path/to/Q4

Step 2 – Make script executable (optional):

chmod +x ransomware.py

Step 3 – Run the script:

sudo python3 ransomware.py

------------------------------------------------------------
Expected Output (Simplified)
------------------------------------------------------------

[+] RUN : openssl rand -base64 16
[+] Symmetric key generated → key.txt

[+] RUN : openssl genrsa -out attacker_private.pem 2048
[+] RUN : openssl rsa -pubout -in attacker_private.pem -out attacker_pub.pem
[+] RSA key-pair generated

[+] RUN : openssl enc -aes-256-cbc ...
[+] my_secrets.txt encrypted → data_cipher.txt

[+] RUN : openssl rsautl -encrypt ...
[+] Symmetric key encrypted → key_cipher.txt

[+] Deleted key.txt
[+] Deleted my_secrets.txt

=== RANSOM NOTE ===
Your file my_secrets.txt is encrypted.
To decrypt it, you need to pay me $10,000 and send key_cipher.txt to me.

------------------------------------------------------------
Files Created
------------------------------------------------------------

- data_cipher.txt        (encrypted secret file – base64)
- key_cipher.txt         (encrypted symmetric key – base64)
- attacker_private.pem   (attacker private key)
- attacker_pub.pem       (attacker public key)

------------------------------------------------------------
What This Demonstrates
------------------------------------------------------------

- Hybrid encryption (AES + RSA)
- Key wrapping using asymmetric crypto
- Use of system-level OpenSSL via subprocess
- Basic ransomware execution flow
- File cleanup after encryption

------------------------------------------------------------
Defensive Relevance
------------------------------------------------------------

This shows why:

- Key management matters
- Strong KDFs should be used (PBKDF2 instead of deprecated defaults)
- Monitoring file modifications is important
- Backups and immutable storage are critical

------------------------------------------------------------
Note
------------------------------------------------------------

This was built strictly for educational use in an isolated VM lab.
Do not use outside controlled environments.