#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2, urllib, json
import codecs
import sys
import datetime
import locale

baseurl = "https://query.yahooapis.com/v1/public/yql?"

yql_query = 'select * from weather.forecast where woeid = 26236758 and u="c"'
# yql_query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="tokyo, jp")'
yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
result = urllib2.urlopen(yql_url).read()
# print result
data = json.loads(result)
# print data['query']['results']

tomorrow = data['query']['results']['channel']['item']['forecast'][1]

#Get info
low = tomorrow['low']
high = tomorrow['high']
image = tomorrow['code']
date = tomorrow['date']
image_url = 'icons/' + image + '.svg'

# Open SVG to process
output = codecs.open('icons/template.svg', 'r', encoding='utf-8').read()

#Read icon (Just the path line)
f = codecs.open(image_url ,'r', encoding='utf-8')
f.readline()
icon = f.readline()
f.close()

# Insert icons and temperatures
us_date = datetime.datetime.strptime(date, '%d %b %Y')
reload(sys)
sys.setdefaultencoding("utf-8") 
locale.setlocale(locale.LC_ALL, ("ja_JP", "utf-8"))
jp_date = us_date.strftime("%_m/%_d(%a)")
output = output.replace('TODAY', jp_date)
output = output.replace('ICON_ONE', icon)
output = output.replace('HIGH_ONE', high)
output = output.replace('LOW_ONE', low)

# Write output
codecs.open('after-weather.svg', 'w', encoding='utf-8').write(output)
