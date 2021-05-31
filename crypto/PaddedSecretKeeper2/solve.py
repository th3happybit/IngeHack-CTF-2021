from pwn import *  
import re 
from base64 import b64decode,b64encode

p = process("./server.py")
# creating the token 
received = p.recvuntil(">").decode()
received_token =re.findall(r"You can use this token to get the secret padding (.*)",received)[0]
p.sendline("1")
p.recvline()
p.sendline("akram")
token = b64decode(received_token)
p.recvuntil(">")

def oracle(token):
    token_b64 = b64encode(token)
    #print(token_b64)
    p.sendline("2")
    p.recvuntil(">>")
    p.sendline(token_b64)
    received = p.recvuntil("Login with your token")
    #print(received)
    return b"Incorrect Padding :- _ -" not in received

cipher_bytearray = bytearray(token)
block_number = len(cipher_bytearray)//16
plaintext = ""
iv_bytearray = bytearray(b'PADDING_ISCARING')

blocks = [cipher_bytearray[16*i:16*i+16]for i in range(block_number)]
for j in range(block_number):
    # get n and n-1 blocks 
    b1 = blocks[block_number-j-1]
    rest = bytearray()
    if j==block_number-1:
        b2 = iv_bytearray
    else:
        b2 = blocks[block_number-j-2]
        for bl in blocks[:block_number-2]:
            rest= rest +bl

    intermediate = bytearray(16)
    cipher_to_flip = bytearray(b2)
    for j in range(16):
        if j!=0 :
            h = 0
            while h<j:
                cipher_to_flip[15-h] = (j+1)^ intermediate[15-h]
                h=h+1
        for i in range(256):
            print(f"Position number: {j} trying out the char number: {i} ")
            if i!= int(b2[15-j]) or j!=0:
                cipher_to_flip[15-j] = i
                cipher_flipped =rest+ cipher_to_flip +b1
                if oracle(cipher_flipped): 
                    print("Found a correct padding")
                    intermediate[15-j] = cipher_to_flip[15-j] ^(j+1)
                    plaintext = chr(b2[15-j]^ intermediate[15-j]) +plaintext
                    print(plaintext)
                    break
p.interactive()