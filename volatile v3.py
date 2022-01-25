import time
import pybithumb
import datetime
import warnings
warnings.filterwarnings('ignore')


# login
f = open("빗썸.txt", "r")
con_key, sec_key = f.readlines()
bithumb = pybithumb.Bithumb(con_key[:-1], sec_key[:-1])  # 개행 삭제

df = pybithumb.get_ohlcv("BTC")

def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    if ticker == "BTC":
        target = today_open + (yesterday_high - yesterday_low) * 0.8
    elif ticker == "ETH":
        target = today_open + (yesterday_high - yesterday_low) * 0.7

    return target


def buy_crypto_currency(ticker):
    print("BUY {}".format(ticker))
    for i in range(10):
        try:
            krw = bithumb.get_balance(ticker)[2]
            krw *= 0.68
            orderbook = pybithumb.get_orderbook(ticker)
            sell_price = orderbook['asks'][0]['price']
            unit = krw/float(sell_price)
            buy = bithumb.buy_market_order(ticker, unit)
        except:
            pass
        time.sleep(0.1)


def sell_crypto_currency(ticker):
    print("SELL {}".format(ticker))
    unit = bithumb.get_balance(ticker)[0]
    sell = bithumb.sell_market_order(ticker, unit)
    print("SELL :", sell)


def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]


now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5_BTC = get_yesterday_ma5("BTC")
ma5_ETH = get_yesterday_ma5("ETH")
target_price_BTC = get_target_price("BTC")
target_price_ETH = get_target_price("ETH")

tickers = ["BTC", "ETH"]
print("watching...")
while True:
    for ticker in tickers:
        try:
            now = datetime.datetime.now()
            if mid < now < mid + datetime.timedelta(seconds=10):
                target_price_BTC = get_target_price("BTC")
                target_price_ETH = get_target_price("ETH")
                mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                ma5_BTC = get_yesterday_ma5("BTC")
                ma5_ETH = get_yesterday_ma5("ETH")
                sell_crypto_currency("BTC")
                sell_crypto_currency("ETH")

            current_price = pybithumb.get_current_price(ticker)
            if ticker == "BTC":
                if (current_price > target_price_BTC) and (current_price > ma5_BTC):
                    buy_crypto_currency("BTC")
            elif ticker == "ETH":
                if (current_price > target_price_ETH) and (current_price > ma5_ETH):
                    buy_crypto_currency("ETH")

        except:
            print("except")

        time.sleep(1)