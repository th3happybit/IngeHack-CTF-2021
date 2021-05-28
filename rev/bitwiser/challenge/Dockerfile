FROM ubuntu:20.04

RUN apt-get update 
RUN apt-get upgrade -y
RUN apt-get install -y socat build-essential manpages-dev

ARG PASSWORD=bitwiser

RUN useradd -m -d /home/bitwiser -s /bin/bash -u 1000 bitwiser
RUN echo "bitwiser:${PASSWORD}" | chpasswd

WORKDIR /home/bitwiser

COPY ./bitwiser.c ./
COPY ./compile.sh ./
COPY ./flag.txt ./

RUN chmod +x ./compile.sh
RUN ./compile.sh

# cleaning up
RUN rm compile.sh

# setup permessions
RUN chown root:bitwiser ./bitwiser && \
    chown root:bitwiser ./flag.txt && \
    chown root:bitwiser ./bitwiser.c

RUN chmod 4550 ./bitwiser &&\ 
    chmod 400 ./flag.txt &&\
    chmod 400 ./bitwiser.c

CMD ["su", "-", "bitwiser", "--command", "socat tcp-listen:9001,fork,reuseaddr EXEC:./bitwiser"]