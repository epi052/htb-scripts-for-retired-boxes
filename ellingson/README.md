# ellingson-exploit.py

Exploits buffer overflow in `garbage` SUID bit binary on HTB's ellingson box.  Bypasses ASLR/NX via Ret2libc.

# Example run on HTB's Ellingson:

`python ellingson-exploit.py`

### Requirements

Needs the `garbage` binary and `libc.so.6` from the target.
