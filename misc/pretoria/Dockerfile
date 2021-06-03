FROM node:16
RUN apt-get update && apt-get install -y \
    socat \
  && rm -rf /var/lib/apt/lists/*

COPY ./app /app

WORKDIR /app
EXPOSE 9999
CMD socat TCP-L:9999,fork,reuseaddr EXEC:"node server.js",stderr
