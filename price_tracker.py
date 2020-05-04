import gspread
import requests
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "client_secret.json", scope)
client = gspread.authorize(creds)
sheet = client.open('product_prices')
#row = ["hey", "i ", "added", "this", "row"]
#sheet.insert_row(row, 3)

csv_data = open("data.csv", "r").read()
client.import_csv(sheet.id, csv_data)


urls = open("urls.txt").read().split("\n")


def get_prices(urls):
    dict = {}
    for url in urls:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        prod_name = soup.find(class_="title-product").get_text().strip()
        price = soup.find(id="price-old")["content"].strip()
        price = int(price.split(".")[0])
        dict[prod_name] = price
    return dict


# print(get_prices(urls))
