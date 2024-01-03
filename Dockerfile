FROM arm32v7/python
# FROM ubuntu:16.04

WORKDIR /wallpaper-server

RUN apt-get update && apt-get install -y librsvg2-bin pngcrush locales-all fonts-takao-gothic cron nginx
# for ubuntu
# RUN apt-get update && apt-get install -y librsvg2-bin pngcrush python2.7 python-pip language-pack-ja-base fonts-takao-gothic cron nginx

# RUN cd /tmp && wget https://www.python.org/ftp/python/3.6.11/Python-3.6.11.tgz && tar zxf Python-3.6.11.tgz && cd Python-3.6.11 && ./configure && make && make install

RUN pip3 install google-api-python-client oauth2client
RUN echo '0 6 * * * root /wallpaper-server/launch.sh' >> /etc/crontab


ADD wallpaper-server /wallpaper-server
ADD .credentials /root/.credentials

EXPOSE 80

CMD service cron start ; /usr/sbin/nginx -g 'daemon off;' -c /etc/nginx/nginx.conf

