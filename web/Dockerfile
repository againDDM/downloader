FROM golang:1.14-buster as go-builder
WORKDIR /go/src/app
RUN go get github.com/lib/pq 
ADD ./src/* ./
RUN go build -o /go/bin/app app


FROM node:13-buster-slim as vue-builder
COPY vue /vue
WORKDIR /vue
RUN npm install -l
RUN npm run build


FROM debian:10-slim
LABEL mainteiner="Vasiliy Badaev <againDDM@gmail.com>"
ARG app_dir="/opt/app"
ARG http_port="5000"
ENV HTTP_PORT=${http_port} \
    APP_DIR=${app_dir} \
    CORS_STRING="*" \
    PGUSER="postgres" \
    PGPASSWORD="postgres" \
    PGHOST="localhost" \
    PGPORT="5432" \
    PGDATABASE="downloader"
WORKDIR $app_dir
EXPOSE ${http_port}
COPY --from=go-builder /go/bin/app ${app_dir}/app
COPY --from=vue-builder /vue/dist ${app_dir}/client
CMD ["./app"]
