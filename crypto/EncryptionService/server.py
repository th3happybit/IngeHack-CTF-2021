#!/usr/bin/python3
from phe import paillier
import traceback
from Crypto.Util.number import bytes_to_long, long_to_bytes


def main():
    public_key, private_key = paillier.generate_paillier_keypair()
    flag = int.from_bytes(open('flag.txt','rb').read(),"big")
    print("Welcome to Our Encryption Service ")
    print("This service allow you to perform either encryption/decryption")
    flag_enc = public_key.encrypt(flag).ciphertext()
    print(flag_enc)
    while True:
        print("Please Select the action to perform: ")
        print("1 - Encrypt ")
        print("2 - Decrypt ")
        action = int(input(">"))
        assert 1<=action<=2
        if action==1:
            print("Input the number you want to encrypt")
            number = int(input(">"))
            if number <0:
                print("Please input  a valid number")
                exit(0)
            try:
                encrypted_number = public_key.encrypt(number)
                print(encrypted_number.ciphertext())
            except ValueError:
                print("Number To High !")
        elif action==2:
            print("Input the number you want to decrypt")
            number = int(input(">"))
            encrypted_number = paillier.EncryptedNumber(public_key,number)
            if number <0:
                print("Please input  a valid number")
                exit(0)
            if number == flag_enc:
                print("So Sorry we can't decrypt this ")
                exit(0)
            try:
                encrypted_number = private_key.decrypt(encrypted_number)
                print(encrypted_number)
            except Exception:
                print('An Erorr has occured you may have passed a wrong number')
            
            
            
if __name__ == '__main__':
    main()
    
