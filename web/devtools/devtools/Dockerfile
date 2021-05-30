FROM node:16-alpine3.11
RUN apk add --no-cache libc6-compat

ENV NODE_ENV production
ENV PORT 3002

EXPOSE 3002

WORKDIR /app

COPY package.json .

RUN yarn
RUN npx next telemetry disable

COPY . .

RUN yarn build

CMD [ "yarn", "start", "-p", "3002"]