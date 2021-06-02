from Crypto.Util.number import *
import random

def nextPrime(prim):
    if isPrime(prim):
        return prim
    else:
        return nextPrime(prim+1)

def generate_robin_prime():
    p = getPrime(512)
    q = nextPrime(p+1)
    # assure the robin's conditions
    while p%4 != 3 or q%4 !=3:
        p = getPrime(512)
        q = nextPrime(p+1)
    return (p,q)

p,q = generate_robin_prime()

n = p*q
m = open('flag.txt').read()
m = bytes_to_long(m)

m = m**e
c = (m*m)%n
c = long_to_bytes(c)
c = c.encode('hex')

cipher = open('cipher','w')
cipher.write(c)