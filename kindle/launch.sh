#! /bin/sh

WALLPAPER_SERVER=10.0.1.199:8080
init_file=/mnt/us/linkss/screensavers/bg_ss00.png
[ -f $init_file ] && rm $init_file
done_file=/mnt/us/linkss/screensavers/done.png
[ -f $done_file ] && rm $done_file
wget -O "$done_file" "http://${WALLPAPER_SERVER}/done.png"
reboot
