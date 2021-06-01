#!/usr/bin/python3 
import base64  
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import traceback
from Crypto.Util.number import  bytes_to_long,long_to_bytes



# We are back with better security 
bit_size = 2048
e = 3


def pad(s):
  return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def isvalidpad(s):
    if s[-1]== 0:
        return False
    return s[-1]*s[-1:]==s[-s[-1]:]

def unpad(s):
    return s[:-s[-1]]

class PaddingError(Exception):
    pass

def make_token(username,type,padding):
    data = {
        "type":type,
        "padding":str(padding),
        "username":username,
    }   
    data_json ="{"+ ";".join([ key+':'+val  for key,val in data.items()])+ "}"
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(data_json).encode("utf-8"))
    token= base64.b64encode(ct)
    return token
    


def menu():
    print("Select one of the following: ")
    print("1) Register a new account ")
    print("2) Login with your token")

def register():
    print("Hey there you are new here right ? ")
    print("Please Submit your Username")
    username = input()
    token = make_token(username,"user", bytes_to_long(os.urandom(4))).decode("utf-8")
    return token



def login():
    global key,iv,SECRET_PADDING,BLOCK_SIZE, rsa_key
    print("Hello There, welcome back !")
    print("To get your secret you need to log in using your token")
    token_enc  = base64.b64decode(input(">>"))
    cipher = AES.new(key, AES.MODE_CBC, iv)
    token_padded  = cipher.decrypt(token_enc)
    try:
        if not isvalidpad(token_padded):
            raise PaddingError()
        token_unpadded = unpad(token_padded).decode('latin-1')
        token = token_unpadded.replace("{","").replace("}","")
        padding = 0
        type ="user"
        for block in token.split(";"):
            if len(block.split(":")) ==2:
                k,value= block.split(":")
                if k=="padding":
                    padding = int(value)
                elif k=="type":
                    type = value
        if type=="root" and padding==SECRET_PADDING:
            flag = open("flag.txt","r").read().encode("utf-8")
            # add some more padding == more security 
            flag_padded= flag +os.urandom(3)
            flag_enc = pow(bytes_to_long(flag_padded),e,rsa_key.n)
            flag_c= long_to_bytes(flag_enc).hex()
            print("Here is your secret keep it warm : ) ")
            print((flag_c,rsa_key.n))
        else:
            print("Here is your secret keep it warm : ) ")
            print("I love IngeHack :!")
    except PaddingError:
        print("Incorrect Padding :- _ - ")
        return 
    


def main():
    print("Welcome To Our Secret Keeper V2 ")
    print("We admit the fact that we have made some mistakes in our first version, but we learned some stuff to be improved")
    print("For that we bought a new system to apply more padding : )")
    token = make_token("user","user",SECRET_PADDING).decode()
    print(f"You can use this token to get the secret padding {token}")
    print("Please You need to authenticate yourself in order to access secrets")
    while True:
        menu()
        choice = int(input(">"))
        assert choice in [1,2]
        if choice == 1:
            token = register()
            print(f"Welcome to the club here is your token {token}")
        elif choice == 2:
            login()




if __name__ == "__main__":
    SECRET_PADDING = bytes_to_long(os.urandom(4))
    BLOCK_SIZE =16
    iv = b'PADDING_ISCARING'
    key = os.urandom(32)
    rsa_key = RSA.generate(bit_size)
    main()