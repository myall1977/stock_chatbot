#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import requests
import json
import datetime
import time
import cPickle
import logging
import sys,os
sys.path.append(os.getcwd()+'/lib')
import day_price,low_high_52w,spreadsheet,telegram_push

kospi_url = 'http://finance.daum.net/xml/xmlallpanel.daum?stype=P&type=S'
kosdaq_url = 'http://finance.daum.net/xml/xmlallpanel.daum?stype=Q&type=S'
log_file = './test.log'
secret_file = './client_secret.json'
spread_sheet_name = 'stocks recommended'
api_token = 'bot540298528:AAFTe6T6tHI-QngptTyr7FH6yDRsKgrBakI'
chat_id = '419480510'
db_base_dir = ''

# Log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 최근 30일의 Price list를 가져오는 함수
def recent_highlow(code):
	# 30일 data를 가져와서 비교 리스트를 만든다.
	day30_raw_list = day_price.gathering_low_high_price(code)
	day30_high = max(map(lambda x: day30_raw_list[x][2],range(30)))
	day30_low = min(map(lambda x: day30_raw_list[x][3],range(30)))
	day10_high = max(map(lambda x: day30_raw_list[x][2],range(10)))
	day10_low = min(map(lambda x: day30_raw_list[x][3],range(10)))
	day5_high = max(map(lambda x: day30_raw_list[x][2],range(5)))
	day5_low = min(map(lambda x: day30_raw_list[x][3],range(5)))
	day1_high = max(map(lambda x: day30_raw_list[x][2],range(1)))
	day1_low = min(map(lambda x: day30_raw_list[x][3],range(1)))
	# 52주 data를 가져와서 비료 리스트를 만든다.
	week52_raw_list = low_high_52w.h_l_52w(code)
	week52_high = week52_raw_list[0]
	week52_low = week52_raw_list[1]
	high_list = [day1_high,day5_high,day10_high,day30_high,week52_high]
	low_list = [day1_low,day5_low,day10_low,day30_low,week52_low]
	return(high_list,low_list)

def current_price_db(_url):
	response = requests.get(_url)
	content = "[" + response.text.split("=")[1].split("[")[1].split("]")[0].strip().replace('\n\t \t\t','').replace('code', '"code"').replace('updn', '"updn"').replace('name', '"name"').replace('cost', '"cost"').replace('rate', '"rate"') + "]"
	j = json.loads(content)
	dict = {}
	for i in range(0,len(j)):
		jsonitem = j[i]
		dict[jsonitem["code"]] = jsonitem["cost"]
	return(dict)

## [[ 추천주 data 정리 ]] ##
# 모카골드 추천주 리스트를 가져온다.
recommend_lists = spreadsheet.moka_price(secret_file,spread_sheet_name)

# 리스트를 code를 키로 한 Dictionary로 다시 만든다.
# 코스피 추천주
ks_recommend_lists = {}
# 코스닥 추천주
kq_recommend_lists = {}
for items in recommend_lists:
	if items['start_price'] is not '':
		s = int(items['start_price'])
	else:
		s = 0
	if items['last_price'] is not '':
		e = int(items['last_price'])
	else:
		e = 0
	gap = ( s - e ) / 4
	first = s
	second = first - gap
	third = second - gap
	forth = third - gap
	fifth = e
	all_list = [items['name'],[first,second,third,forth,fifth]]

	if items['category'] == 'kospi':
		ks_recommend_lists[str(items['code']).rjust(6,"0")] = all_list
	else:
		kq_recommend_lists[str(items['code']).rjust(6,"0")] = all_list

print ks_recommend_lists

## [[ 현재가 DB 만들기 ]] ##
stock_price_db = current_price_db(kospi_url)
stock_price_db.update(current_price_db(kosdaq_url))

print stock_price_db

# 추천주 Code list를 만든다.
recommend_codes = ks_recommend_lists.keys() + kq_recommend_lists.keys()

# 시작해볼까요?
for code in recommend_codes:
	# 현재가 조사
	current_price = int(stock_price_db[code].replace(",",""))
	# high low list 만들기 (단 1일에 한번)
        print recent_highlow(code)
	# 추천가 정리
