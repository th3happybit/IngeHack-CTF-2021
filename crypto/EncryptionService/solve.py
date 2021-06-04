from pwn import *
import  re
from Crypto.Util.number import long_to_bytes
r = process("./server.py")
received = r.recvuntil('>').decode('utf-8')
flag_enc = int(re.findall(r'\d+', received)[0])

def encrypt(data):
    r.sendline(str(1))
    received = r.recvuntil('>').decode('utf-8')
    r.sendline(str(data))  
    received = r.recvuntil('>').decode('utf-8')
    if 'Number To High !' in received:
        return -1
    else:
        enc = re.findall(r'\d+', received)[0]
        return int(enc)

def decrypt(data):
    r.sendline(str(2))
    received = r.recvuntil('>').decode('utf-8')
    r.sendline(str(data))  
    received = r.recvuntil('>').decode('utf-8')
    dec = int(re.findall(r'\d+', received)[0])
    return dec

def find_N():
    # length of N should be similar to the length of the secret
    start = 10**610
    end = 10**620
    # binary search
    while start < end:
        mid = (start + end) // 2
        res = encrypt(mid)
        if res == None:
            # server sends 'None' for 0 and n-1
            return mid + 1
        if res == -1:
            end = mid
        else:
            start = mid + 1
        print(f'[{start}, {end}]')
    return start
n_3 =  find_N()
for i in range(10):
    n = n_3*3 +i
    e_1 = encrypt(1)
    k = (flag_enc*e_1) %pow(n,2)
    fl = decrypt(k)
    print(long_to_bytes(fl))

