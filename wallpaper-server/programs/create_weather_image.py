#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request, json
import codecs
import sys
import datetime
import locale
import re

import secrets

url = "https://api.openweathermap.org/data/2.5/forecast/daily?q=Tokyo,jp&appid={}&lang=ja&units=metric&cnt=2".format(secrets.APPID)
result = urllib.request.urlopen(url).read()
# print result
data = json.loads(result)
# print(data)
# print data['forecasts'][1]

tomorrow = data['list'][1]

#Get info
low   = str(int(tomorrow["temp"]["min"]))
high  = str(int(tomorrow["temp"]["max"]))
description = tomorrow['weather'][0]['description']
image_num = str(tomorrow['weather'][0]['id'])
light = tomorrow["weather"][0]["icon"][-1:]

image_url = 'icons/' + str(image_num) + light + '.svg'
date = datetime.datetime.fromtimestamp(tomorrow['dt'])

# Open SVG to process
output = codecs.open('icons/template.svg', 'r', encoding='utf-8').read()

#Read icon (Just the path line)
f = codecs.open(image_url ,'r', encoding='utf-8')
f.readline()
icon = f.readline()
f.close()

# Insert icons and temperatures
# reload(sys)
# sys.setdefaultencoding("utf-8")
locale.setlocale(locale.LC_ALL, ("ja_JP", "utf-8"))
jp_date = date.strftime("%_m/%_d(%a)")
output = output.replace('TODAY', jp_date)
output = output.replace('ICON_ONE', icon)
output = output.replace('HIGH_ONE', high)
output = output.replace('LOW_ONE', low)
output = output.replace('WEATHER_TEXT', description)

# Write output
codecs.open('after-weather.svg', 'w', encoding='utf-8').write(output)
