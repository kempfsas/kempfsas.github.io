# Statisches Portfolio, ausgeliefert von nginx.
FROM nginx:1.27-alpine

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

COPY index.html 404.html /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/
COPY work/   /usr/share/nginx/html/work/
COPY blog/   /usr/share/nginx/html/blog/

EXPOSE 8080
