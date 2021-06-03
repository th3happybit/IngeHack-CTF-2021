#!/bin/bash

socat -dd -T60 TCP-LISTEN:8000,reuseaddr,fork,su=encryptor2 EXEC:/home/encryptor2/encryptor2,stderr
