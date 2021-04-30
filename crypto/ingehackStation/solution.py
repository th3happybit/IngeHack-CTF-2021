from pwn import * 
from Crypto.Util.number import inverse
import re 
from ecdsa import SigningKey, VerifyingKey,NIST256p
import string
from ecdsa.ecdsa import Signature

curve = NIST256p
G = curve.generator
n = curve.order

# launch the challenge
r = process("./station.py")
received  = r.recvuntil('> ').decode()
public_badge = re.findall(r'Here is your public badge of the day \((\d+),(\d+)\)', received)[0]

# here we save all the signature we received
saved_signatures = {}
while True:
    # sign message 
    r.sendline('2')
    r.recvuntil('What do you want to be signed ? :')
    # generate random message to be signed 
    message = ''.join(random.choice(string.ascii_letters) for i in range(10)) 
    r.sendline(message)
    # receive signature
    received = r.recvuntil('> ').decode()
    signature = re.findall(r'Here is your autograph \(r,s\) go show it to your friends \((\d+),(\d+)\)', received)[0]
    # get the r part of (r,s) signature 
    r_sign = int(signature[0])
    # check if we have a collision ( signature with a nonce reuse)
    if r_sign in saved_signatures.keys():
        s1 = saved_signatures[r_sign][0]
        h1 = saved_signatures[r_sign][1]
        s2 = int(signature[1])
        h2 = int(hashlib.sha256(message.encode()).hexdigest(),16)
        # this loop will just allow us to test different combinations  s1-s2 s1+s2 -s1+s2 -s1-s2
        k = (h1 - h2) * inverse((s1 - s2) % n, n) % n
        # calculate private key 
        p = (s1 * k - h1) * inverse(r_sign,n) % n
        signing_key = SigningKey.from_secret_exponent(p, curve=curve, hashfunc="sha256")
        # Verify if build key is appropriate
        if signing_key.get_verifying_key().pubkey.verifies(h1, Signature(r_sign, s1)) and signing_key.get_verifying_key().pubkey.verifies(h2, Signature(r_sign, s2)):
            r.sendline('1')
            r.recvuntil('> ')
            r.sendline('4')
            r.recvuntil('=>')
            r.sendline(str(p))
            r.interactive()
            break        
    saved_signatures[r_sign] = (int(signature[1]),int(hashlib.sha256(message.encode()).hexdigest(),16))
