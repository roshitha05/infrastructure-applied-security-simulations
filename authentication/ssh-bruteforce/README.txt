# SSH Brute Force (Lab Simulation)

This script performs a simple dictionary-based brute-force attack against an SSH server using Python and Paramiko.

It was developed in a controlled lab environment (Kali + Metasploitable2) to understand how weak authentication mechanisms can be exploited.

---

## What it does

- Takes target IP, username, and a password list (10 entries)
- Tries each password sequentially
- Stops when the correct password is found
- Executes `whoami` to verify successful login

The script disables key-based authentication so only password login is tested.

---

## Why this matters

If SSH is exposed and protected only by weak passwords, it becomes an easy entry point.

This is especially risky in:
- Public-facing servers
- Poorly configured cloud instances
- Systems without rate limiting or lockout policies

---

## How to run

```bash
python3 sshbf.py <target_ip> <username> <password_list.txt>