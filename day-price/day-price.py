import requests
import time
 
from bs4 import BeautifulSoup

def gathering_low_high_price(stockItem):
  price_list = []
  for page in range(1, 4):
    url = 'http://finance.naver.com/item/sise_day.nhn?code=' + stockItem +'&page='+ str(page)
    html = requests.get(url)
    source = BeautifulSoup(html.text, "html.parser")
    srlists=source.find_all("tr")
    isCheckNone = None
     
    if((page % 1) == 0):
      time.sleep(1.50)
   
    for i in range(1,len(srlists)-1):
      if(srlists[i].span != isCheckNone):
        srlists[i].td.text
        date = srlists[i].find_all("td",align="center")[0].text
        end_price = int(srlists[i].find_all("td",class_="num")[0].text.replace(",",""))
        high_price = int(srlists[i].find_all("td",class_="num")[3].text.replace(",",""))
        low_price = int(srlists[i].find_all("td",class_="num")[4].text.replace(",",""))
        price_list.append([date, end_price, high_price, low_price])
  return(price_list)

if __name__ == '__main__':
  stockItem = '005930'
  print gathering_low_high_price(stockItem)

