FROM python:3.7

ENV DISCORD_TOKEN=ODQ5NzU3MTIyMzIwNzkzNjIw.YLfz_Q.RHdAlGX5yE02rnxM4wrEZSsngMw

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install -r requirements.txt && \
    rm -f requirements.txt

RUN mkdir /chall 
WORKDIR /chall 

COPY ./bot.py .



RUN chown -R nobody:nogroup .

USER nobody

ENTRYPOINT ["python3", "-u", "bot.py"]