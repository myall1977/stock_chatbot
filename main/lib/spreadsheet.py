import gspread
from oauth2client.service_account import ServiceAccountCredentials

def moka_price(secret,sheet_name):
    # use creds to create a client to interact with the Google Drive API
    #scope = ['https://spreadsheets.google.com/feeds']
    scope = ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(secret, scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(sheet_name).sheet1
    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    return(list_of_hashes)

if __name__ == '__main__':
    print(moka_price('../client_secret.json','stocks recommended'))
