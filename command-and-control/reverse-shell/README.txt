# Reverse Shell (Lab Simulation)

This module implements a simple reverse shell using Python sockets.

The idea:
The server listens.
The client connects back.
Commands typed on the server are executed on the client machine.

Built and tested in a controlled Kali Linux lab environment.

------------------------------------------------------------
What this version supports
------------------------------------------------------------

This version properly handles the `cd` command.

Normally, reverse shells fail with `cd` because each command runs in a new subprocess.
Here, directory changes are handled using os.chdir() so the working directory persists.

Communication between server and client uses:
- JSON for structured command exchange
- Base64 encoding to safely transmit command output

------------------------------------------------------------
Files
------------------------------------------------------------

server.py      -> Listener (command sender)
revshell.py    -> Client (connects back and executes commands)

Make sure both files use the same IP address and port.

------------------------------------------------------------
How to Run (Lab Only)
------------------------------------------------------------

Open TWO terminals.

Terminal 1 – Start the listener:

cd /path/to/Q3
sudo python3 server.py

You should see:
Listening...

------------------------------------------------------------

Terminal 2 – Start the reverse shell client:

cd /path/to/Q3
sudo python3 revshell.py

If successful, Terminal 1 will show:
Connection from (<IP>, <port>) established.
shell>

------------------------------------------------------------
Example Usage (from Terminal 1)
------------------------------------------------------------

shell> whoami
root

shell> pwd
/media/sf_369/a1/Q3

shell> cd ..
shell> pwd
/media/sf_369/a1

To close the session:
shell> quit

------------------------------------------------------------
What This Demonstrates
------------------------------------------------------------

- Reverse connection behaviour (client initiates connection)
- Remote command execution
- Basic command-and-control logic
- Persistent working directory handling (cd support)

------------------------------------------------------------
Defensive Relevance
------------------------------------------------------------

Reverse shells are commonly used in post-exploitation scenarios.

This highlights the importance of:
- Monitoring outbound connections
- Egress filtering
- Detecting unusual TCP sessions
- Logging command execution activity

------------------------------------------------------------
Note
------------------------------------------------------------

For educational use in controlled lab environments only.
Do not use on systems without authorization.