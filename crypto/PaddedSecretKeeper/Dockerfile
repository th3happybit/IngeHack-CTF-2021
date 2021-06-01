FROM python:3.8-alpine3.12

RUN apk --update add gcc build-base freetype-dev \
    libpng-dev openblas-dev \
    socat tcpdump 

RUN addgroup -S chall && adduser -S chall -G chall

RUN mkdir /chall 
WORKDIR /chall 

COPY ./flag.txt ./
COPY ./requirements.txt ./ 
COPY ./server.py ./ 
COPY ./start.sh ./


RUN chown -R root:chall /chall && \
    chmod 750 /chall && \
    chmod 400 /chall/flag.txt && \
    chmod 550 /chall/server.py && \
    chmod 550 /chall/start.sh






RUN pip3 install -r requirements.txt

CMD ["./start.sh"]

EXPOSE 9999