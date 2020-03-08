FROM node:13-buster-slim as vue-builder
COPY vue /vue
WORKDIR /vue
RUN npm install -l
RUN npm run build

FROM python:3.7-slim-buster
LABEL mainteiner="Vasiliy Badaev <vbadaev@tradingview.com>"
ARG app_dir="/opt/application"
WORKDIR $app_dir
ENV DOWNLOADS_DIR="/opt/downloads" 
RUN DEBIAN_FRONTEND=noninteractive \
    apt update && \
    apt install sqlite3 -y && \
    pip3 install youtube-dl \
                 flack \
                 flask_cors \
                 gunicorn && \
    apt autoremove -y && \
    apt clean
EXPOSE 5000
ADD src/downloader.py src/application.py src/wsgi.py src/run.sh ./
COPY --from=vue-builder /vue/dist ${app_dir}
CMD ["sh", "run.sh"]
