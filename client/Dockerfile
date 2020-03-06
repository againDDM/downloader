FROM node:13-buster-slim as build-stage
RUN mkdir -p /vue
COPY vue/package*.json ./
RUN npm install -l
COPY vue /vue
WORKDIR /vue
RUN npm run build

FROM nginx:1.17
LABEL mainteiner="Vasiliy Badaev <vbadaev@tradingview.com>"
COPY --from=build-stage /vue/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
