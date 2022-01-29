import pybithumb
import numpy as np
import warnings
import time
import datetime
import pandas as pd
warnings.filterwarnings('ignore')


# login
f = open("빗썸.txt", "r")
con_key, sec_key = f.readlines()
bithumb = pybithumb.Bithumb(con_key[:-1], sec_key[:-1])  # 개행 삭제


def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    a = bithumb.sell_market_order(ticker, unit)
    print("SELL {}".format(ticker), a)


tickers = pybithumb.get_tickers()

for ticker in tickers:
    sell_crypto_currency(ticker)