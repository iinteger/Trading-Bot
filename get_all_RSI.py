import pybithumb
import numpy as np
import pandas as pd
import warnings
from tqdm import tqdm
warnings.filterwarnings("ignore")

# BTC ETH ADA
tickers = pybithumb.get_tickers()

buying_ticker = ["NPT"]

for ticker in tqdm(tickers):
    df = pybithumb.get_ohlcv(ticker)
    df = pd.concat([df["2022"]], axis=0)

    df['변화량'] = df['close'] - df['close'].shift(1)
    df['상승폭'] = np.where(df['변화량'] >= 0, df['변화량'], 0)
    df['하락폭'] = np.where(df['변화량'] < 0, df['변화량'].abs(), 0)

    # welles moving average
    df['AU'] = df['상승폭'].ewm(alpha=1 / 14, min_periods=14).mean()
    df['AD'] = df['하락폭'].ewm(alpha=1 / 14, min_periods=14).mean()
    # df['RS'] = df['AU'] / df['AD']
    # df['RSI'] = 100 - (100 / (1 + df['RS']))
    df['RSI'] = df['AU'] / (df['AU'] + df['AD']) * 100

    if df["RSI"][-1] <= 30 or df["RSI"][-2] <= 30:
        print("Under RSI 30 :", ticker)
