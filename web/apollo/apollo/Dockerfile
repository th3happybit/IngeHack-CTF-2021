FROM node:16-alpine3.11
RUN apk add --no-cache libc6-compat

ENV NODE_ENV production
ENV PORT 3000

EXPOSE 3000

WORKDIR /home/nextjs/app

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

COPY package.json .

RUN chown -R nextjs:nodejs /home/nextjs

USER nextjs

RUN yarn
RUN npx next telemetry disable

COPY . .

RUN yarn build

CMD [ "yarn", "start" ]