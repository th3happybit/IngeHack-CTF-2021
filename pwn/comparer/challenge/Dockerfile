FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y openssh-server --no-install-recommends
RUN apt-get install -y python3 python-is-python3 --no-install-recommends

ARG PASSWORD=comparer

RUN useradd -m -d /home/comparer -s /bin/bash -u 1000 comparer
RUN echo "comparer:${PASSWORD}" | chpasswd

WORKDIR /home/comparer

COPY ./Makefile ./
COPY ./comparer.c ./
COPY ./flag.txt ./
COPY ./comparer ./

RUN chown -R root:comparer /home/comparer && \
    chmod 750 /home/comparer && \
    chmod 400 /home/comparer/flag.txt && \
    chmod 444 /home/comparer/Makefile && \
    chmod 444 /home/comparer/comparer.c && \
    chmod 550 /home/comparer/comparer && \
    chmod u+s /home/comparer/comparer

RUN service ssh start
CMD ["/usr/sbin/sshd","-D"]

EXPOSE 22
