#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time
import cPickle
import logging
import sys,os
sys.path.append(os.getcwd()+'/lib')
import day_price,low_high_52w,spreadsheet,telegram_push

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

# 모카골드 추천주 리스트를 가져온다.
recommend_lists = spreadsheet.moka_price(secret_file,spread_sheet_name)
# 리스트를 code를 키로 한 Dictionary로 다시 만든다.
ks_recommend_lists = {}
kq_recommend_lists = {}
for items in recommend_lists:
	if items['category'] == 'kospi':
		ks_recommend_lists[str(items['code']).rjust(6,"0")] = [items['name'],items['start_price'],items['last_price']]
	else:
		kq_recommend_lists[str(items['code']).rjust(6,"0")] = [items['name'],items['start_price'],items['last_price']]
print(ks_recommend_lists)
