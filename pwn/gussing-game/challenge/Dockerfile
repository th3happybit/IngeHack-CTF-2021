FROM ubuntu:20.04

RUN apt-get update 
RUN apt-get upgrade -y
RUN apt-get install -y socat build-essential manpages-dev

ARG PASSWORD==gusser

RUN useradd -m -d /home/gusser -s /bin/bash -u 1000 gusser
RUN echo "gusser:${PASSWORD}" | chpasswd

WORKDIR /home/gusser

COPY ./gusser.c ./
COPY ./Makefile ./
COPY ./flag.txt ./

RUN make

# setup permessions
RUN chown root:root ./flag.txt && \
    chown root:gusser ./gusser.c && \
    chown root:gusser ./gusser

RUN chmod 400 ./flag.txt &&\
    chmod 440 ./gusser.c && \
    chmod 4410 ./gusser

CMD ["su", "-", "gusser", "--command", "socat tcp-listen:9001,fork,reuseaddr EXEC:./gusser"]