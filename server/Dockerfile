FROM node:13-buster-slim as vue-builder
COPY vue /vue
WORKDIR /vue
RUN npm install -l
RUN npm run build

FROM python:3.8-slim-buster
ARG app_dir="/opt/application"
WORKDIR "$app_dir"
ENV DOWNLOADS_DIR="/opt/downloads" 
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update \
    && apt-get install -y \
        sqlite3 \
        ffmpeg \
    && python -m pip --no-cache-dir install \
        youtube-dl \
        flack \
        flask_cors \
        gunicorn \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf "/var/lib/apt/lists/*"
EXPOSE 5000
ADD "src/downloader.py" "src/application.py" "src/wsgi.py" "src/run.sh" ./
COPY --from=vue-builder "/vue/dist" "${app_dir}"
CMD ["sh", "run.sh"]
