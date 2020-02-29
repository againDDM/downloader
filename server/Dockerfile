FROM python:3.7-slim-buster
LABEL mainteiner="Vasiliy Badaev <vbadaev@tradingview.com>"
ARG app_dir="/opt/application"
WORKDIR $app_dir
ENV DOWNLOADS_DIR="/opt/downloads" \
    SQLITE_PATH="/opt/application/app-db.sqlite3"
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
ADD src/application.py src/wsgi.py src/run.sh ./
ADD src/static ./static
CMD ["sh", "run.sh"]
