from Crypto.Cipher import ARC4


key = b"AAABC"
offset = 256 + 8 * 33
enc_stack = b'+\xefQ^'
payload = b"A" * offset + enc_stack

rc4 = ARC4.new(key)

c = rc4.encrypt(payload)
print(c[offset:])
