#!/bin/sh

cd "$(dirname "$0")"

# don't need docker env
# . env/bin/activate
python3 programs/create_weather_image.py
python3 programs/create_events_image.py
sed -i -e 's/&/&amp;/g' almost_done.svg

rsvg-convert -w 758 -h 1024 --background-color=white -o almost_done.png almost_done.svg

#We optimize the image
pngcrush -c 0 almost_done.png done.png

#We move the image where it needs to be
done_file=/var/www/html/done.png
[ -f $done_file ] && rm $done_file
mv done.png $done_file

rm after-weather.svg
rm almost_done.png
rm almost_done.svg*

