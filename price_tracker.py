import os
import smtplib
import time
from collections import OrderedDict
from datetime import date
from email.message import EmailMessage

import gspread
import requests
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

#     EMAIL_ID = "mohit.khanwale1@gmail.com"
#     EMAIL_PASSWORD = "imubqnckgkuqcqsb"
#BASE = "C:\\Users\\MohiT\\Desktop\\Python_Projects\\price_tracker\\"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "client_secret.json", scope)

shareable_sheet_link = "https://docs.google.com/spreadsheets/d/1-9eXx4mr4kexJ4CiMlkf4YP0QP4ixQZw6bJ2qQRP6w8/edit?usp=sharing"


# TO DO-
# 1. --- DONE --- EMAIL
# 2. Different websites
# 3. Graph
# 4. GUI
# 5. --- DONE --- Schedule Script
# 6. --- DONE --- Add functionality to delete products


def get_prices(urls):
    dict = OrderedDict()
    for url in urls:
        try:
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            prod_name = soup.find(class_="title-product").get_text().strip()
            price = soup.find(id="price-old")["content"].strip()
            price = int(price.split(".")[0])

        except Exception:
            dict["Could not retrieve- "+url] = "NA"
            continue

        dict[prod_name] = price
    return dict


def add_to_sheets(dic, client):
    today = date.today()
    timestamp = time.strftime('%H:%M')
    day = today.strftime("%B %d, %Y")

    sheet = client.open('product_prices').sheet1
    sheet_empty = True
    if sheet.get_all_values():
        col_count = len(sheet.get_all_values()[0])
        sheet_empty = False
    prod_names = list(dic.keys())
    prices = list(dic.values())
    prod_names.insert(0, "Products/Dates")
    prices.insert(0, day+" - "+timestamp)
    #  IF THE SHEET IS EMPTY - Add product names as the first row.
    if sheet_empty is True:
        sheet.insert_row(prod_names, 1)
    # IF NEW PRODUCTS ARE ADDED- Delete the existing product names and add the updated prod list.
    # Products can only be added at the end of the text file
    elif col_count < len(prod_names):
        sheet.delete_rows(1)
        sheet.insert_row(prod_names, 1)
    # IF ANY PRODUCT GETS DELETED- Delete column
    elif col_count > len(prod_names):
        row1 = sheet.row_values(1)
        deleted_products = list(set(row1)-set(prod_names))
        for i in deleted_products:
            ind = row1.index(i)
            sheet.delete_columns(ind+1)
    # APPEND THE PRODUCT PRICES AT THE END
    row_count = len(sheet.get_all_values())
    sheet.insert_row(prices, row_count+1)


def send_email(message):
    EMAIL_ID = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PRICE_TRACKER_APP_PASS")
    msg = EmailMessage()
    msg['Subject'] = 'Price Dropped for some of your products!'
    msg['From'] = EMAIL_ID
    msg['To'] = EMAIL_ID
    msg.set_content(message)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ID, EMAIL_PASSWORD)
        smtp.send_message(msg)


def check_if_price_lower(dic, client):
    sheet = client.open('product_prices').sheet1
    row_count = len(sheet.get_all_values())
    if row_count <= 2:
        return "Insufficent Data to compare"
    prod_names = list(dic.keys())
    old_prices = sheet.row_values(row_count-1)
    del old_prices[0]
    new_prices = list(dic.values())
    price_lowered = False
    message = ["Price dropped for following product(s)-"]
    num = 1
    if len(old_prices) != len(new_prices):
        return "Cannot compare!"
    for i in range(len(old_prices)):
        if old_prices[i] and new_prices[i] and old_prices[i] != "NA" and new_prices[i] != "NA":
            if new_prices[i] < int(old_prices[i]):
                price_lowered = True
                diff = int(old_prices[i])-new_prices[i]
                message.append(str(num) + ". " + prod_names[i] + "\nPrice dropped by- Rs " +
                               str(diff) + "\nCurrent Price- Rs " + str(new_prices[i]) + "\nShop here- " + urls[i])
                num += 1
                print("Price Dropped for product - "+prod_names[i])
    if price_lowered is True:
        msg = "\n\n".join(message)
        send_email(msg)
        print("Email sent to user!")


if __name__ == "__main__":
    client = gspread.authorize(creds)
    urls = open("urls.txt").read().split("\n")
    diction = get_prices(urls)
    print(diction)
    add_to_sheets(diction, client)
    check_if_price_lower(diction, client)
    print("Google sheet updated Successfully!")
    print("View the google sheet at-", shareable_sheet_link)
