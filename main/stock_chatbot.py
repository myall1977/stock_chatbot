#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import requests
import json
import datetime
import time
import cPickle
import logging
import logging.handlers
import sys,os
import datetime

base_dir = '/home/myall1977_2/stock_chatbot/main/'
sys.path.append(base_dir + 'lib')
import realtime_prices,spreadsheet,telegram_push

reload(sys)
sys.setdefaultencoding('utf-8')

log_file = base_dir + 'stock_chatbot.log'
secret_file = base_dir + 'client_secret.json'
spread_sheet_name = 'stocks recommended'
api_token = 'bot540298528:AAFTe6T6tHI-QngptTyr7FH6yDRsKgrBakI'
#chat_id = '419480510'
chat_id = '-1001202493867'
database_filename = base_dir + 'stock_status.db'
trans = ["추천가접근","정찰대","선발대","본대","후발대","지하"]

## 현재시간
dt = datetime.datetime.now()

## Log
# 로거 인스턴스를 만든다
logger = logging.getLogger('mylogger')

# 포매터를 만든다
fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

# 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
fileHandler = logging.FileHandler(log_file)
streamHandler = logging.StreamHandler()

# 각 핸들러에 포매터를 지정한다.
fileHandler.setFormatter(fomatter)
streamHandler.setFormatter(fomatter)

# 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
logger.addHandler(fileHandler)
#logger.addHandler(streamHandler)

logger.setLevel(logging.INFO)


# 현재 가격과 추천가격과 비교
def price_compare(code,c_price):
    load_all_price = recommend_lists_dics[code][1]
    cur_index = -1
    for index_no in range(0,6):
        if c_price > load_all_price[index_no]:
            break
        else:
            cur_index = index_no
    return cur_index

if __name__ == '__main__':
    try:
        logger.info("Start Analysis stock data")
        ## [[ 추천주 data 정리 ]] ##
        # 모카골드 추천주 리스트를 가져온다.
        logger.debug("Update Moka recommend stock prices")
        recommend_lists = spreadsheet.moka_price(secret_file,spread_sheet_name)
        # 리스트를 code를 키로 한 Dictionary로 다시 만든다.
        # 코스피 추천주
        recommend_lists_dics = {}
        for items in recommend_lists:
            if items['first_price'] is not '':
                s = int(items['first_price'].replace(",",""))
            else:
                s = 0
            if items['last_price'] is not '':
                e = int(items['last_price'].replace(",",""))
            else:
                e = 0
            gap = ( s - e ) / 4
            first = s
            second = first - gap
            third = second - gap
            forth = third - gap
            last = e
            near = int(first*1.05)
            all_list = [items['name'],[near,first,second,third,forth,last]]

            recommend_lists_dics[str(items['code']).rjust(6,"0")] = all_list

        ## [[ 현재가 DB 만들기 ]] ##
        ## 현재가를 Dics로 검색함.
        # {{{{stock_price_db}}}} dictionary로 현재가를 search하세요.
        logger.debug("Getting realtime stock price")
        stock_price_db = realtime_prices.current_price("kospi")

        # 추천주 Code list를 만든다.
        recommend_codes = recommend_lists_dics.keys()

        # 추천주 Status DB file을 읽어온다.
        # {{{{status_db}}}} dictionary로 예전의 Index를 search하세요. 
        logger.debug("Reading stock status database")
        if os.path.exists(database_filename):
            try:
                db_f = open(database_filename,"r")
                status_db = cPickle.load(db_f)
                db_f.close()
            except Exception as ex:
                logger.error(ex)
                sys.exit()
        else:
            status_db = {}
            for _code in recommend_codes:
                status_db[_code] = 0

        logger.debug("Starting analysis the prices")
        # 신규 측정된 DB
        new_status_db = {}
        # 요약본을 보낼 DB
        summary_db = {}
        # 시작해볼까요?
        for code in recommend_codes:
            # 종목명
            jongmok_name = recommend_lists_dics[code][0]
            logger.debug(jongmok_name)

            # 현재가 조사
            current_price = stock_price_db[code]
            logger.debug(current_price)
            
            # 해당 종목의 현재/과거의 가격위치
            current_index = price_compare(code,current_price)
            logger.debug(current_index)
            if code in status_db:
                previous_index = status_db[code]
            else:
                previous_index = 0
            logger.debug(previous_index)
            
            logger.debug("stock code / current price : %s / %s"%(code,current_price)) 
            logger.debug("current index / previous index : %s / %s"%(current_index,previous_index))
            
            # Output message를 Generation 합니다.
            send_msg = 0
            if current_index > previous_index :
                send_msg = 1
                output_msg = jongmok_name + " : " + trans[current_index] + " 진입"

            elif current_index < previous_index :
                send_msg = 1
                if current_index is -1 :
                    output_msg = jongmok_name + " : " + "추천가 모니터링 해제"
                else :
                    output_msg = jongmok_name + " : " + trans[previous_index] + " 이탈\n" + jongmok_name + " : " + trans[current_index] + " 진입"

            if send_msg is 1 :
                output_msg = output_msg + "\n" + "현재가(매수구간) : %d(%d,%d,%d,%d)"%(current_price,recommend_lists_dics[code][1][1],recommend_lists_dics[code][1][2],recommend_lists_dics[code][1][3],recommend_lists_dics[code][1][4])
                logger.info(output_msg)
                result = telegram_push.send_msg(api_token,chat_id,output_msg)
                logger.info(result)
            if current_index > 0:
                if current_index in summary_db.keys():
                    summary_db[current_index] = summary_db[current_index] + "%s : %d\n"%(jongmok_name,current_price)
                else:
                    summary_db[current_index] = "%s : %d\n"%(jongmok_name,current_price)

            new_status_db[code] = current_index
        logger.debug("Update stock status database")
        db_f = open(database_filename,"w")
        cPickle.dump(new_status_db,db_f)
        db_f.close()


        # Test
        if dt.hour in [23,3,6,7]:
            if dt.minute in [0]:
                logger.info("Send summary")
                summary_output_msg = ""
                for _index in summary_db.keys():
                    summary_output_msg = summary_output_msg + "== %s ==\n%s\n"%(trans[_index],summary_db[_index])
                result = telegram_push.send_msg(api_token,chat_id,summary_output_msg)
                logger.debug(summary_output_msg)
                logger.info(result)
        logger.info("All processes done")
    except Exception as ex:
        logger.error(ex)
        #result = telegram_push.send_msg(api_token,chat_id,ex)
        logger.info(result)
        sys.exit()
