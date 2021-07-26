FROM alpine:3.14
RUN apk add curl
CMD curl http://es:9200
