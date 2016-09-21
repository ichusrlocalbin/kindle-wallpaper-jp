FROM hypriot/rpi-node
# FROM ubuntu:16.04

ADD wallpaper-server /wallpaper-server
ADD .credentials /root/.credentials

WORKDIR /wallpaper-server

RUN apt-get update
RUN apt-get install -y librsvg2-bin pngcrush python2.7 python-pip locales-all fonts-takao-gothic cron nginx
# for ubuntu
# RUN apt-get update && apt-get install -y librsvg2-bin pngcrush python2.7 python-pip language-pack-ja-base fonts-takao-gothic cron nginx
RUN pip install google-api-python-client
RUN echo '0 6 * * * root /wallpaper-server/launch.sh' >> /etc/crontab

EXPOSE 80

CMD service cron start ; /usr/sbin/nginx -g 'daemon off;' -c /etc/nginx/nginx.conf

