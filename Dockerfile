FROM node:lts-alpine

RUN npm install -g json-server

WORKDIR /data
VOLUME /data

COPY products-db-1x.json /default-db.json
COPY routes.json /routes.json

EXPOSE 8080
COPY run.sh /run.sh
ENTRYPOINT ["sh", "/run.sh"]
CMD []
