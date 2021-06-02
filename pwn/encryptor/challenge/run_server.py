import threading
import socketserver
import os
import sys

import ingecryptor

BUFFER_SIZE = 1024


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # I couldn't see my C/C++ extension output
        # I managed to see the output using this file descriptor hacks
        socket_fd = self.request.fileno()
        os.dup2(socket_fd, 1)
        os.dup2(socket_fd, 2)

        # if have all the luck of the world you will get the flag
        world_luck = os.urandom(16)

        self.request.send(
            b"choose an option:\n1) Try your luck\n2) Try our fast RC4 implementation\n"
        )
        option = self.request.recv(BUFFER_SIZE).decode().strip()
        if option == "1":
            self.request.send(b"Can you guess the next 16 bytes from /dev/urandom ?\n")
            random_bytes = self.request.recv(BUFFER_SIZE)
            if random_bytes != os.urandom(16):
                self.request.send(b"You did it, enjoy your flag: \n")
                ingecryptor.get_flag()
            else:
                self.request.send(b"It is obvious, you can't do that.\n")
        elif option == "2":
            self.request.send(b"Key: \n")
            key = self.request.recv(BUFFER_SIZE)
            self.request.send(b"Data: \n")
            data = self.request.recv(BUFFER_SIZE)
            response = ingecryptor.rc4(key, data)
            self.request.sendall(response)
        else:
            self.request.send(b"Invalid option\n")


class ThreadedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8000

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    print("Server loop running in process:", os.getpid(), file=sys.stderr)
    server.serve_forever()
