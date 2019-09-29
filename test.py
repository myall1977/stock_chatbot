#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup

url = 'http://www.truewarrant.com/elw/search/search.jsp'
data = {'gb1_1':'2001'}
file = '/var/www/html/result.html'
head = """<html>
<head>
<title>ELW price</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
<table>
"""
footer = """
</table>
</body>
</html>
"""
body = ""
jongmoks = ['00003','00005']
durations = ['1','2']

def getData(jongmok,duration):
    min = 0
    max = 0
    nextKey = ''
    _body = ''

    while True:
        data['gb2_1'] = jongmok
        data['gb4_1'] = duration
	data['nextKey'] = nextKey
        html = requests.post(url,data)
        source = BeautifulSoup(html.text, "html.parser")
        target_list = source.findAll(attrs={'name':'data_check'})
        if not target_list:
            break
        else:
            for l in target_list:
                _body = _body + str(l.findParent().findParent())
            if min is 0 and max is 0:
                nextKey = '00000|00031'
                min = 0
                max = 31
            else:
                min = max
                max = max + 30
                nextKey = '%s|%s'%(str(min).zfill(5),str(max).zfill(5))
        time.sleep(0.5)
    return(_body)

for duration in durations:
    for jongmok in jongmoks:
        body = body + getData(jongmok,duration)

final_content = body
final_content = final_content.replace('<td width="1"></td>','')
print final_content
