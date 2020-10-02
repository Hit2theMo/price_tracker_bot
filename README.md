# Product Price Tracker - An Amazing Project

Python web scraper to Track Prices of different PC Parts from various Indian PC part websites like [MDcomputers](https://mdcomputers.in/), etc. \
If price is lowered for any of the products, an Email is sent to the user with information of products whose prices are dropped. \
All prices are also updated on a **Google spreadsheet** using the Sheets API.
This google sheet is available [here](https://docs.google.com/spreadsheets/d/1-9eXx4mr4kexJ4CiMlkf4YP0QP4ixQZw6bJ2qQRP6w8/edit?usp=sharing). \
This Scraper is deployed on **Heroku** to run every few hours daily.


## Screenshots
#### Google Spreadsheet-
![image](https://user-images.githubusercontent.com/34605049/81412230-2f524f00-9161-11ea-865f-808ff8eecf63.png "Prices updated in Google Spreadsheet" )

#### Sample Email sent to user-
<img src="https://user-images.githubusercontent.com/34605049/81412687-d7681800-9161-11ea-87b4-0f2a4ee9bc10.png" height="400" >

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install requirements.txt
```

## Packages used
1. **Requests** - To scrap websites
2. **Gspread** - To update Google Sheets
3. **BeautifulSoup** - To access HTML of the web page
4. **Oauth2client** - To connect to the Google APIs
5. **Schedule** - To schedule the scraper to run daily on heroku.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

