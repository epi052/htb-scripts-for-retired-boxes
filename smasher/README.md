# tiny-web-server Exploit  

## Requirements

- [pwntools](https://github.com/Gallopsled/pwntools)
- libc downloaded from target (`targets-libc`)
- tiny-web-server downloaded from server (`tiny`)

## Execution

```
git clone https://github.com/epi052/htb-scripts-for-retired-boxes.git
cd htb-scripts-for-retired-boxes/smasher
python tiny-web-server-exploit.py
```

# Padding Oracle Buster 

## Requirements

- [python-paddingoracle](https://github.com/mwielgoszewski/python-paddingoracle)

## Execution

```
git clone https://github.com/epi052/htb-scripts-for-retired-boxes.git
cd htb-scripts-for-retired-boxes/smasher
python smasher-padding-oracle.py -b 16 'irRmWB7oJSMbtBC4QuoB13DC08NI06MbcWEOc94q0OXPbfgRm+l9xHkPQ7r7NdFjo6hSo6togqLYITGGpPsXdg==' 10.10.10.89
```

# Race Condition Privesc

## Execution

Upload script to target or type it out, etc...

```
git clone https://github.com/epi052/htb-scripts-for-retired-boxes.git
cd htb-scripts-for-retired-boxes/smasher

... get escalate.sh to target ...

chmod u+x escalate.sh
./escalate.sh 
```