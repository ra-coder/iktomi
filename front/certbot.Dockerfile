FROM certbot/certbot:latest
COPY ./nginx/iktomi.conf /etc/nginx/conf.d/.