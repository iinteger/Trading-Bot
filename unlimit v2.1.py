# 무한매수법 코인버전
# 시드 : 400만
# 일일 거래금액 : 10만원

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

    if bithumb.get_balance(ticker)[2] < 10000000:
        krw = int(krw / 2)

    print("BUY")
    try:
        orderbook = pybithumb.get_orderbook(ticker)
        sell_price = orderbook['asks'][0]['price']
        unit = krw / float(sell_price)
        buy = bithumb.buy_market_order(ticker, unit)
        ticker_balance += krw
    except:
        pass


def set_price_per_unit(bithumb, ticker):
    global ticker_balance

    unit = bithumb.get_balance(ticker)[0]
    unit = int(unit * 10000) / 10000
    price_per_unit = ticker_balance / unit

    return price_per_unit


# login
def main(ticker, balance):
    f = open("빗썸.txt", "r")
    con_key, sec_key = f.readlines()
    bithumb = pybithumb.Bithumb(con_key[:-1], sec_key[:-1])  # 개행 삭제
    global ticker_balance
    ticker_balance = balance  # 현재  잔고의 매수금액으로 설정

    ticker = ticker
    price_per_unit = set_price_per_unit(bithumb, ticker)
    sell_five_persent = False

    now = datetime.datetime.now()
    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
    print("종목 : {}".format(ticker))
    print("평단 : {}".format(price_per_unit))
    while True:
        try:
            now = datetime.datetime.now()

            # 매수, LOC 매도
            if mid < now < mid + datetime.timedelta(seconds=10):
                sell_five_persent = False
                mid = now + datetime.timedelta()  # 시간 갱신
                print("\n\n{}. {} {}=========================================".format(now.month, now.day, ticker))

                # 전반전
                if ticker_balance <= 2000000:
                    # 큰수매수
                    if pybithumb.get_current_price(ticker) <= price_per_unit*1.05:
                        buy_crypto_currency(bithumb, ticker, 50000)
                        print("큰수매수로 50000원 구매")

                    # 평단매수
                    if pybithumb.get_current_price(ticker) <= price_per_unit:
                        buy_crypto_currency(bithumb, ticker, 50000)
                        print("평단매수로 50000원 구매")

                    # LOC매도
                    if pybithumb.get_current_price(ticker) >= price_per_unit*1.05:
                        unit = bithumb.get_balance(ticker)[0]
                        bithumb.sell_market_order(ticker, unit/4)
                        ticker_balance = int(ticker_balance*3/4)
                        print("LOC매도로 {}개 판매".format(unit/4))
                        print("예상수익 :", unit/4*pybithumb.get_current_price(ticker))

                # 후반전
                else:
                    # 매수
                    if pybithumb.get_current_price(ticker) <= price_per_unit:
                        buy_crypto_currency(bithumb, ticker, 100000)
                        print("평단매수로 100000원 구매")

                    # LOC매도
                    if pybithumb.get_current_price(ticker) >= price_per_unit:
                        unit = bithumb.get_balance(ticker)[0]
                        bithumb.sell_market_order(ticker, unit/4)
                        ticker_balance = int(ticker_balance * 3 / 4)
                        print("LOC매도로 {}개 판매".format(unit/4))
                        print("예상수익 :", unit/4*pybithumb.get_current_price(ticker))

                # 구매, LOC매도 후 평단 조정
                unit = bithumb.get_balance(ticker)[0]
                price_per_unit = set_price_per_unit(bithumb, ticker)
                print("총 구매수량 :", unit)
                print("평단 :", price_per_unit)

            time.sleep(3)
            # 매도 : after 지정가는 상시 감시
            # 전반전
            if ticker_balance <= 2000000:
                if pybithumb.get_current_price(ticker) >= price_per_unit*1.1:
                    unit = bithumb.get_balance(ticker)[0]
                    bithumb.sell_market_order(ticker, unit)
                    ticker_balance = 0
                    print("LOC매도로 {}개 판매".format(unit / 4))
                    print("예상수익 :", unit / 4 * pybithumb.get_current_price(ticker))

                    unit = bithumb.get_balance(ticker)[0]
                    price_per_unit = set_price_per_unit(bithumb, ticker)
                    print("총 구매수량 :", unit)
                    print("평단 :", price_per_unit)

            # 후반전
            else:
                if sell_five_persent == False and pybithumb.get_current_price(ticker) >= price_per_unit*1.05:
                    unit = bithumb.get_balance(ticker)[0]
                    bithumb.sell_market_order(ticker, unit/4)
                    sell_five_persent = True
                    ticker_balance = int(ticker_balance*3/4)
                    print("after 지정가 매도로 {}개 판매".format(unit / 4))
                    print("예상수익 :", unit / 4 * pybithumb.get_current_price(ticker))

                    unit = bithumb.get_balance(ticker)[0]
                    price_per_unit = set_price_per_unit(bithumb, ticker)
                    print("총 구매수량 :", unit)
                    print("평단 :", price_per_unit)

                elif pybithumb.get_current_price(ticker) >= price_per_unit*1.1:
                    unit = bithumb.get_balance(ticker)[0]
                    bithumb.sell_market_order(ticker, unit)
                    ticker_balance = 0
                    print("after 지정가 매도로 {}개 판매".format(unit))
                    print("예상수익 :", unit * pybithumb.get_current_price(ticker))

                    unit = bithumb.get_balance(ticker)[0]
                    price_per_unit = set_price_per_unit(bithumb, ticker)
                    print("총 구매수량 :", unit)
                    print("평단 :", price_per_unit)

            time.sleep(1)

        except Exception as e:
            print("except", e)

        time.sleep(2)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))  # ticker, balance