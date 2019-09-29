#!/usr/bin/env python 
import requests


def h_l_52w(stockItem):
    url = 'http://finance.daum.net/item/ajax/checkprice.daum?code=' + stockItem
    json_data = requests.get(url)
    if json_data.status_code is 200 :
        high52wk = int(json_data.text.split("high52wk: '")[1].split("'")[0])
        low52wk = int(json_data.text.split("low52wk: '")[1].split("'")[0])
    else :
        high52wk = ''
        low52wk = ''
    return([high52wk,low52wk])

if __name__ == '__main__':
    stockItem = '005930'
    print h_l_52w(stockItem)
