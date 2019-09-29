import requests

def send_msg(token,chat_id,msg):
    telegram_begin_url = 'https://api.telegram.org/'
    telegram_middle_url = '/sendMessage?chat_id='
    telegram_end_url = '&text='
    api_url = telegram_begin_url + token + telegram_middle_url + chat_id + telegram_end_url + msg
    r = requests.get(api_url)
    return(r.status_code)

if __name__ == '__main__':
    api_token = 'bot540298528:AAFTe6T6tHI-QngptTyr7FH6yDRsKgrBakI'
    chat_id = '419480510'
    message = 'push test'
    print(send_msg(api_token,chat_id,message))
