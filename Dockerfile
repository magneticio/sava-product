FROM node:lts-alpine

RUN npm install -g json-server

WORKDIR /data
VOLUME /data

ADD products-db-1x.json /default-db.json
ADD routes.json /routes.json

EXPOSE 8080
ADD run.sh /run.sh
ENTRYPOINT ["sh", "/run.sh"]
CMD []
