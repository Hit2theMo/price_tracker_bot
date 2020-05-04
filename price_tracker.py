import gspread
import requests
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date


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


def add_to_sheets(dic, client):
    sheet = client.open('product_prices').sheet1
    row_count = len(sheet.get_all_values())
    prod_names = list(dic.keys())
    prices = list(dic.values())
    prod_names.insert(0, "Products/Dates")
    prices.insert(0, day)
    #sheet.insert_row(prod_names, 2)
    sheet.insert_row(prices,row_count+1)


if __name__ == "__main__":
    today = date.today()
    day = today.strftime("%B %d, %Y")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "client_secret.json", scope)
    client = gspread.authorize(creds)

    urls = open("urls.txt").read().split("\n")

    dic = get_prices(urls)
    print(dic)
    add_to_sheets(dic, client)
    print("Google sheet updated Successfully!")
    print("View the google sheet at- https://docs.google.com/spreadsheets/d/1-9eXx4mr4kexJ4CiMlkf4YP0QP4ixQZw6bJ2qQRP6w8/edit?usp=sharing")
