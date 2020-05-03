import requests
from bs4 import BeautifulSoup

urls = ["https://mdcomputers.in/amd-hexa-core-ryzen-5-3600.html",
        "https://mdcomputers.in/msi-rx-5700-xt-mech-oc-8gb-gddr6.html",
        "https://mdcomputers.in/galax-rtx-2060-super-ex-1-click-oc-8gb-gddr6-26isl6mpx2ex.html"
        ]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}

for url in urls:
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    prod_name = soup.find(class_="title-product").get_text().strip()
    price = soup.find(id="price-old")["content"].strip()
    price = int(price.split(".")[0])
    print(prod_name)
    print(price)
