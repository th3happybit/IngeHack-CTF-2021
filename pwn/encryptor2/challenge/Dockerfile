FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat --no-install-recommends

RUN useradd -m -d /home/encryptor2 -s /bin/bash -u 1000 encryptor2

WORKDIR /home/encryptor2

COPY ./flag.txt ./
COPY ./encryptor2 ./

RUN chown -R root:encryptor2 /home/encryptor2 && \
    chmod 750 /home/encryptor2 && \
    chown root:encryptor2 /home/encryptor2/flag.txt && \
    chmod 440 /home/encryptor2/flag.txt && \
    chmod 550 /home/encryptor2/encryptor2

EXPOSE 8000

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
