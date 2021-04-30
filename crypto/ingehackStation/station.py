#!/usr/bin/python 
import random 
import ecdsa
import hashlib
import time
from Crypto.Util.number import inverse
BITS_LENGTH = 16
MOD = 2**9

curve = ecdsa.NIST256p
G = curve.generator
n = curve.order

# make it a dict a key and description 
games = {
    "Batman: Arkham Origins":"Live like Batman and Protect Gotham City from the evil !",
    "GTA IV":"Welcome To Liberty City A place where you have to do some shitty work to live",
    "Uncharted 2":"After being tracked down by Harry Flynn, Nathan Drake goes on a quest for Marco Polo's lost fleet. However when things take an unexpected turn for the worst, Drake must rely on those closest to him in order to find the Cintomani Stone.",
    "IngeHack 2": "You never know what you are missing : ) "
}

def generate_random():
    r = random.randint(2**BITS_LENGTH,2**(BITS_LENGTH+1))
    return r+2**BITS_LENGTH  % MOD 

def print_intro(public_badge):
    print("==================   Welcome To IngeHack Station  ===================")
    print("To ensure the security of our station we are using a special ***secure*** system")
    print("Here is your public badge of the day ({},{})".format(int(public_badge.x()), int(public_badge.y())))
    print("Our system has proven to be unbreakable ! Don't waste your time and enjoy playing")

def show_welcome_menu():
    print("===========================================================")
    print("===============    Welcome Screen  ========================")
    print("===========================================================")
    print("To Start of you have the possibility to either play a game or get a digital Autograph from our Awesome Team :) ")
    print("1 - Play Game")
    print("2 - Get An Autograph")


def show_game_menu():
    print("===========================================================")
    print("=================    Game List  ===========================")
    print("===========================================================")
    print("Select the game number you want to play with ")
    for iterator, game in enumerate(games.items()):
        print(" Game: {} ===>  {} -  {}".format(iterator+1,game[0], game[1]))
    

def play_game(game_number,badge):
    # premium game 
    if game_number == 4:
        print("This is a PREMIUM Game you need to prove you are a premium member by showing us your private badge")
        priv_badge = int(input("=> "))
        if priv_badge == badge:
            print(open("flag.txt",'r').read())
        else:
            print("Hacker Detected ! Good Try: ) BYE")
    else:
        game_name = list(games.items())[game_number-1][0]
        print("...... Launching Game {} .......".format(game_name))
        time.sleep(1)
        print("ENJOY PLAYING {} ! BY IngehackStation ".format(game_name))

def sign_autograph(priv_badge):
    m1 = input("What do you want to be signed ? : ").encode()
    h1 = int(hashlib.sha256(m1).hexdigest(),16)
    done = False
    while not done:
        k = generate_random()
        P = k*G
        r = P.x()%n
        if r == 0:
            continue
        s = inverse(k,n)*(h1+r*priv_badge)%n
        if s == 0:
            continue
        done = True
    print("Here is your autograph (r,s) go show it to your friends ({},{})".format(r,s))


def main():
    private_badge = random.randint(1,n-1)
    public_badge = G*private_badge
    print_intro(public_badge)
    while True:
        show_welcome_menu()
        mode = int(input("> ")) 
        assert  1<=mode<=2
        if mode ==1 :
            show_game_menu()
            game_number = int(input("> "))
            assert 1<=game_number<=len(games)
            play_game(game_number,private_badge)
            exit(0)
        else:
            sign_autograph(private_badge)


if __name__ == '__main__':
    main()