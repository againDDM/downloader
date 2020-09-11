FROM node:13-buster-slim as vue-builder
COPY vue /vue
WORKDIR /vue
RUN npm install -l
RUN npm run build

FROM nginx/unit:1.19.0-python3.7
WORKDIR "/opt/application"
ENV DOWNLOADS_DIR="/opt/downloads"
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev \
        python3-pip \
        python3-setuptools \
        sqlite3 \
        ffmpeg \
    && python3 -m pip --no-cache-dir install \
        youtube-dl \
        alembic \
        flack \
        flask_cors \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf "/var/lib/apt/lists/*"
EXPOSE 5000
ADD "src/downloader.py" "src/application.py" "src/wsgi.py" ./
ADD "config.json" "run.sh" /docker-entrypoint.d/
COPY --from=vue-builder "/vue/dist" "/opt/application"
