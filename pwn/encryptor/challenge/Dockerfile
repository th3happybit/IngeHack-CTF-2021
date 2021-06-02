FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python-is-python3 python3-pip --no-install-recommends
RUN python -m pip install -U pip

RUN useradd -m -d /home/comparer -s /bin/bash -u 1000 ingecryptor

WORKDIR /home/ingecryptor

COPY ingecryptor-0.0.1-cp38-cp38-linux_x86_64.whl ./
RUN python -m pip install ./ingecryptor-0.0.1-cp38-cp38-linux_x86_64.whl

COPY ./flag.txt ./

RUN chown -R root:ingecryptor /home/ingecryptor && \
    chmod 750 /home/ingecryptor && \
    chown root:ingecryptor /home/ingecryptor/flag.txt && \
    chmod 440 /home/ingecryptor/flag.txt

EXPOSE 8000

COPY entrypoint.sh /
COPY run_server.py /
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
