#!/bin/bash

socat -dd -T60 TCP-LISTEN:8000,reuseaddr,fork,su=encryptor EXEC:/home/encryptor/encryptor,stderr
