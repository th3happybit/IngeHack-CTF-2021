FROM node:16-alpine3.11

RUN mkdir /app
COPY app /app
WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_ENV production

RUN yarn

RUN chown -R root:node /app/ 

USER node

EXPOSE 3000
CMD ["yarn", "start"]