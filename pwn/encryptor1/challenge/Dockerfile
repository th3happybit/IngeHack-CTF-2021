FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat --no-install-recommends

RUN useradd -m -d /home/encryptor -s /bin/bash -u 1000 encryptor

WORKDIR /home/encryptor

COPY ./flag.txt ./
COPY ./encryptor ./

RUN chown -R root:encryptor /home/encryptor && \
    chmod 750 /home/encryptor && \
    chown root:encryptor /home/encryptor/flag.txt && \
    chmod 440 /home/encryptor/flag.txt && \
    chmod 550 /home/encryptor/encryptor

EXPOSE 8000

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
