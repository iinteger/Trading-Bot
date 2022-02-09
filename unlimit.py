import time
import pybithumb
import datetime
import warnings
import numpy as np
import pandas as pd
import sys
warnings.filterwarnings('ignore')


def buy_crypto_currency(bithumb, ticker, krw):
    global ticker_balance

    print("BUY")
    try:
        orderbook = pybithumb.get_orderbook(ticker)
        sell_price = orderbook['asks'][0]['price']
        unit = krw / float(sell_price)
        buy = bithumb.buy_market_order(ticker, unit)
        ticker_balance += krw
    except:
        pass


def set_target_price(bithumb, ticker):
    global ticker_balance

    unit = bithumb.get_balance(ticker)[0]
    unit = int(unit * 10000) / 10000
    price_per_unit = ticker_balance / unit

    print("평단 :", price_per_unit)
    balance = bithumb.get_balance(ticker)[3]

    if balance < 1000000:  # 100만원 이하로 남으면
        target_price = price_per_unit * 1.035
        stoploss_price = price_per_unit * 0.95
    else:
        target_price = price_per_unit * 1.05
        stoploss_price = price_per_unit * 0.96

    stop_buy_price = price_per_unit * 1.03


    if target_price < 1:
        target_price = int(target_price * 10**4) / 10**4
    elif target_price < 10:
        target_price = int(target_price * 10**3) / 10**3
    elif target_price < 100:
        target_price = int(target_price * 10**2) / 10**2
    elif target_price < 1000:
        target_price = int(target_price * 10**1) / 10**1
    elif target_price < 5000:
        target_price = int(target_price)
    elif target_price < 10000:
        target_price = int(target_price // 5 * 5)
    elif target_price < 50000:
        target_price = int(target_price // 10 * 10)
    elif target_price < 100000:
        target_price = int(target_price // 50 * 50)
    elif target_price < 500000:
        target_price = int(target_price // 100 * 100)
    elif target_price < 1000000:
        target_price = int(target_price // 500 * 500)
    else:
        target_price = int(target_price // 1000 * 1000)

    return target_price, stoploss_price, stop_buy_price


def get_RSI(ticker):
    df = pybithumb.get_candlestick(ticker, chart_intervals="1h")  # 1시간봉
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


# login
def main(ticker, balance):
    f = open("빗썸.txt", "r")
    con_key, sec_key = f.readlines()
    bithumb = pybithumb.Bithumb(con_key[:-1], sec_key[:-1])  # 개행 삭제
    global ticker_balance
    ticker_balance = balance  # 현재  잔고의 매수금액으로 설정

    target_price = np.inf
    stoploss_price = -1
    stop_buy_price = np.inf
    ticker = ticker

    now = datetime.datetime.now()
    mid = now + datetime.timedelta(seconds=5)  # 지금 매매 시작
    #mid = now + datetime.timedelta(hours=1)  # 한시간 뒤 매매 시작

    print("watching...")


    while True:
        try:
            now = datetime.datetime.now()
            # 정기 매매
            if mid <= now < mid + datetime.timedelta(seconds=20):
                print("\n\n{} 정기 매수=========================================".format(ticker))
                mid = now + datetime.timedelta(hours=1)  # 시간 갱신

                if pybithumb.get_current_price(ticker) > stop_buy_price:
                    print("수익률 3% 이상으로 매수 X")
                    continue

                RSI = get_RSI(ticker)[-1]
                if RSI > 70:
                    buy_crypto_currency(bithumb, ticker, 3000)
                elif RSI > 60:
                    buy_crypto_currency(bithumb, ticker, 5000)
                elif RSI > 50:
                    buy_crypto_currency(bithumb, ticker, 7000)
                elif RSI > 40:
                    buy_crypto_currency(bithumb, ticker, 10000)
                else:
                    buy_crypto_currency(bithumb, ticker, 15000)

                time.sleep(1)
                print("총 구매금액 :", ticker_balance)

                unit = bithumb.get_balance(ticker)[0]
                target_price, stoploss_price, stop_buy_price = set_target_price(bithumb, ticker)

                print("총 구매수량 :", unit)
                print("목표가 :", target_price)

            time.sleep(5)
            # 물타기 매매
            if pybithumb.get_current_price(ticker) < stoploss_price:
                print("\n\n{} 물타기 매매========================================".format(ticker))
                buy_crypto_currency(bithumb, ticker, 5000)
                time.sleep(1)
                print("총 사용금액 :", ticker_balance)

                unit = bithumb.get_balance(ticker)[0]
                target_price, stoploss_price, stop_buy_price = set_target_price(bithumb, ticker)

                print("총 구매수량 :", unit)
                print("목표가 :", target_price)

            time.sleep(5)
            # 매도
            if pybithumb.get_current_price(ticker) > target_price and bithumb.get_balance(ticker)[0] > 10:
                unit = bithumb.get_balance(ticker)[0]
                bithumb.sell_market_order(ticker, unit)

                print("\n\n{} 매도========================================".format(ticker))
                print("판매수량 :", unit)
                print("목표가격 :", target_price)
                print("총 구매금액", ticker_balance)
                print("예상 판매가격 :", unit*target_price)

                ticker_balance = 0
                target_price = np.inf
                stoploss_price = -1
                stop_buy_price = np.inf

        except Exception as e:
            print("except", e)

        time.sleep(1)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))  # ticker, balance