import requests
import json


def current_price(market):
    kospi_url = 'http://finance.daum.net/xml/xmlallpanel.daum?stype=P&type=S'
    kosdaq_url = 'http://finance.daum.net/xml/xmlallpanel.daum?stype=Q&type=S'
    if market is "kospi":
        _url = kospi_url
    else:
        _url = kosdaq_url
    response = requests.get(_url)
    if market in ["kospi","kosdaq"]:
        content = "[" + response.text.split("=")[1].split("[")[1].split("]")[0].strip().replace('\n\t \t\t','').replace('code', '"code"').replace('updn', '"updn"').replace('name', '"name"').replace('cost', '"cost"').replace('rate', '"rate"') + "]"
        j = json.loads(content)
        dict = {}
        for i in range(0,len(j)):
            jsonitem = j[i]
            dict[jsonitem["code"]] = int(jsonitem["cost"].replace(",",""))
    return(dict)

if __name__ == '__main__':
    print current_price("kosdaq")
