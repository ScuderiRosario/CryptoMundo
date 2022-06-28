import pandas as pd
import yfinance as yf
import datetime
from datetime import date, timedelta

def download(CryptoName):
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    end_date = d1
    d2 = date.today() - timedelta(days=360)
    d2 = d2.strftime("%Y-%m-%d")
    start_date = d2
    crypto=CryptoName
    crypto=crypto+'-eur'
    data = yf.download(crypto,start=start_date, end=end_date, progress=False)
    return data

