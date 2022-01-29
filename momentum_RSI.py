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

target_rate = 1.02
loss_rate = 0.95


def buy_crypto_currency(ticker):
    krw = 2000
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw / float(sell_price)
    unit = int(unit*10000)/10000
    a = bithumb.buy_market_order(ticker, unit)
    print("BUY {}".format(ticker), a)


# 추매함수
def buy_accumulate(ticker):
    krw = 1000
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw / float(sell_price)
    unit = int(unit*10000)/10000
    a = bithumb.buy_market_order(ticker, unit)
    print("accumulate BUY {}".format(ticker), a)


def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    a = bithumb.sell_market_order(ticker, unit)
    print("SELL {}".format(ticker), a)


def get_RSI(ticker):
    df = pybithumb.get_candlestick(ticker, chart_intervals="1m")  # 분봉
    delta = df["close"].diff()

    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    period = 14
    au = ups.ewm(com=period - 1, min_periods=period).mean()
    ad = downs.abs().ewm(com=period - 1, min_periods=period).mean()

    RS = au / ad
    RSI = pd.Series(100 - (100 / (1 + RS)))

    return RSI


def dict_to_txt(purchased):
    f = open("purchased.txt", "w")

    for i in purchased:
        f.write(str(i) + " : " + str(purchased[i]) + "\n")
    f.close()


tickers = pybithumb.get_tickers()
traiding_time = [0, 10, 20, 30, 40, 50]
purchased = {}  # ticker : [high, low, accumulated_cash]
print("watching...")

while True:
    now = datetime.datetime.now()
    if now.minute in traiding_time:
        for ticker in tickers:
            try:
                current_price = pybithumb.get_current_price(ticker)
                if ticker in purchased:
                    if purchased[ticker][0] <= current_price:  # 목표가 달성
                        sell_crypto_currency(ticker)
                        del purchased[ticker]
                        dict_to_txt()

                    elif purchased[ticker][1] >= current_price:  # 손실가 달성
                        pre_balance = bithumb.get_balance("BTC")[2]
                        buy_accumulate(ticker)
                        post_balance = bithumb.get_balance("BTC")[2]
                        paid = post_balance-pre_balance
                        purchased[ticker][2] += paid

                        unit = bithumb.get_balance(ticker)[0]
                        total_paid = purchased[ticker][2]
                        average_price = total_paid/unit
                        purchased[ticker][0] = average_price * target_rate
                        purchased[ticker][1] = average_price * loss_rate
                        dict_to_txt()

                else:  # 구매된 종목이 아닐때
                    df = pybithumb.get_candlestick(ticker, chart_intervals="1m")
                    close = df["close"]

                    ma60 = close.rolling(60).mean()[-1]
                    ma10 = close.rolling(10).mean()[-1]
                    ma5 = close.rolling(5).mean()[-1]

                    RSI = get_RSI(ticker)
                    RSI_MA10 = RSI.rolling(10).mean()

                    print(ticker)
                    print(current_price > ma5 > ma10 > ma60)
                    print(RSI[-1] < RSI_MA10[-1])
                    print(RSI[-1] < 60)

                    if (current_price > ma5 > ma10 > ma60) and (RSI[-1] < RSI_MA10[-1]) and (RSI[-1] < 60):
                        pre_balance = bithumb.get_balance("BTC")[2]
                        buy_crypto_currency(ticker)
                        post_balance = bithumb.get_balance("BTC")[2]
                        paid = post_balance-pre_balance

                        high = current_price * target_rate
                        low = current_price * loss_rate
                        purchased[ticker] = [high, low, paid]
                        dict_to_txt()

            except:
                pass
        time.sleep(2)
    time.sleep(1)