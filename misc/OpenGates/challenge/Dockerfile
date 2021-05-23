# sudo docker build -t opengates:1.0 .
# sudo docker run -d -p 31337:31337 --rm -it opengates:1.0

FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y build-essential libssl-dev --no-install-recommends

RUN groupadd -g 1000 -p guest guest
RUN useradd -d /home/guest/ -m -u 1000 -g 1000 -p guest -s /bin/bash guest
RUN echo "guest:guest" | chpasswd

WORKDIR /home/guest

COPY OpenGates.c .
COPY customPasswds .
COPY Makefile .
COPY flag .
COPY ynetd .

#Compiling
RUN make

RUN chown -R root:guest /home/guest && \
    chmod 750 /home/guest && \
    chmod 400 /home/guest/flag && \
    chmod 400 /home/guest/customPasswds && \
    chmod 444 /home/guest/Makefile && \
    chmod 444 /home/guest/OpenGates.c && \
    chmod 550 /home/guest/OpenGates && \
    chmod u+s /home/guest/OpenGates


USER guest
EXPOSE 31337
CMD ./ynetd -se y -p 31337 ./OpenGates
