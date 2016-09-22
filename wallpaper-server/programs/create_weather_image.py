#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2, urllib, json
import codecs
import sys
import datetime
import locale
import re

query = "city=130010"

livedoor_yahoo_map = {
    1: 32, 2: 30, 3: 40, 4: 16, 5: 26, 6: 40, 7: 16, 8: 28, 9: 28,
    10: 11, 11: 16, 12: 28, 13: 11, 14: 16, 15: 11, 16: 40, 17: 11, 18: 5, 19: 40,
    20: 11, 21: 5, 22: 45, 23: 16, 24: 16, 25: 16, 26: 16, 27: 16, 28: 16, 29: 16, 30: 16
}

baseurl = "http://weather.livedoor.com/forecast/webservice/json/v1?"
query_url = baseurl + query
result = urllib2.urlopen(query_url).read()
# print result
data = json.loads(result)
# print data['forecasts'][1]

tomorrow = data['forecasts'][1]

#Get info
low = tomorrow['temperature']['min']['celsius'].encode('utf-8')
high = tomorrow['temperature']['max']['celsius'].encode('utf-8')
description = tomorrow['telop'].encode('utf-8')
livedoor_image_url = tomorrow['image']['url'].encode('utf-8')
livedoor_image_num = int(re.search('^http://weather.livedoor.com/img/icon/(\d+).gif$', livedoor_image_url).group(1))
date = tomorrow['date'].encode('utf-8')
# print(low, high, description, image_num, date)
image_num = livedoor_yahoo_map[livedoor_image_num]
image_url = 'icons/' + str(image_num) + '.svg'

# Open SVG to process
output = codecs.open('icons/template.svg', 'r', encoding='utf-8').read()

#Read icon (Just the path line)
f = codecs.open(image_url ,'r', encoding='utf-8')
f.readline()
icon = f.readline()
f.close()

# Insert icons and temperatures
orig_date = datetime.datetime.strptime(date, '%Y-%m-%d')
reload(sys)
sys.setdefaultencoding("utf-8")
locale.setlocale(locale.LC_ALL, ("ja_JP", "utf-8"))
jp_date = orig_date.strftime("%_m/%_d(%a)")
output = output.replace('TODAY', jp_date)
output = output.replace('ICON_ONE', icon)
output = output.replace('HIGH_ONE', high)
output = output.replace('LOW_ONE', low)
output = output.replace('WEATHER_TEXT', description)

# Write output
codecs.open('after-weather.svg', 'w', encoding='utf-8').write(output)
