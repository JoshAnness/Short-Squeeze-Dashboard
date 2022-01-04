import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from datetime import timedelta
from ratelimit import limits

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

pd.set_option('display.max_colwidth', 25)
url = 'https://finviz.com/screener.ashx?v=131&f=sh_short_o30&o=-shortinterestshare'
response = Request(url, headers = headers)
webpage = urlopen(response).read()
html = soup(webpage, "html.parser")
data = pd.read_html(str(html))[-2]

pages = html.find_all('a', {'class':'screener-pages'})
pageCount = 1
for page in pages:
    pageCount += 1

end = 1
j = 0;

for i in range(pageCount):
    if i > 0:
        end += 20
        url = 'https://finviz.com/screener.ashx?v=131&f=sh_short_o30&o=-shortinterestshare' + '&r=' + str(end)
        response = Request(url, headers = headers)
        webpage = urlopen(response).read()
        holder = soup(webpage, "html.parser")
        hold = pd.read_html(str(holder))[-2]
        hold = hold.drop(0)
        array = pd.DataFrame(hold).to_numpy()
        data = pd.concat([data, pd.DataFrame(array)])

data = data.drop(data.columns[[0]], axis=0)

data.columns = [
    "No.",
    "Ticker",
    "Market Cap",
    "Outstanding",
    "Float",
    "Insider Own",
    "Insider Trans",
    "Inst Own",
    "Inst Trans",
    "Float Short",
    "Short Ratio",
    "Avg Volume",
    "Price",
    "Change",
    "Volume"
]

data = data.drop(labels="No.", axis=1)

#@limits(calls = 9, period = timedelta(seconds = 60).total_seconds())
def getBorrowData(ticker):
    url = 'https://iborrowdesk.com/api/ticker/' + ticker.lower()
    try:
        data = requests.get(url).json()
        df = pd.DataFrame(data['real_time'])
        s = df['available']
        availableShares = s[0]
        s = df['fee']
        fee = s[0]
        availableShares = str(availableShares)
        fee = str(fee)
        array = np.array([availableShares, fee])
    except:
        return
    return array

data['Available Shares'] = ''
data['Borrowing Fee'] = ''
0
for index, row in data.iterrows():
    try:
        arr = getBorrowData(row['Ticker'])
        data.at[index, 'Available Shares'] = arr[0]
        data.at[index, 'Borrowing Fee'] = arr[1]
    except:
        pass

data.head(20)
