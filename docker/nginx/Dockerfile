FROM nginx:1.22.0

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/nginx/nginx.conf /etc/nginx/conf.d
# COPY ./docker/nginx/nginx.conf /etc/nginx/templates/default.conf.template