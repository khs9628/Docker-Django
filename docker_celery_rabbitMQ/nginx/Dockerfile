FROM nginx:latest

RUN mkdir /etc/nginx/geoip
RUN rm /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/nginx.conf


COPY nginx.conf /etc/nginx/
COPY nginx-app.conf /etc/nginx/conf.d/
COPY GeoIP.dat /etc/nginx/geoip/

