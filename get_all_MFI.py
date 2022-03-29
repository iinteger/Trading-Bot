import pybithumb
import numpy as np
import pandas as pd
import warnings
from tqdm import tqdm
warnings.filterwarnings("ignore")

# BTC ETH ADA
tickers = pybithumb.get_tickers()

buying_ticker = ["DAI", "NPT"]

for ticker in tqdm(tickers):
    #df = pybithumb.get_ohlcv("XRP")
    df = pybithumb.get_ohlcv(ticker)
    df = pd.concat([df["2022"]], axis=0)

    close_price = df["close"].values
    low_price = df["low"].values
    high_price = df["high"].values
    volume = df["volume"].values

    MF = volume[1:] * (high_price[1:]+low_price[1:]+close_price[1:]) / 3
    PMF = np.zeros(len(MF))
    NMF = np.zeros(len(MF))

    PMF[close_price[1:] > close_price[:-1]] = MF[close_price[1:] > close_price[:-1]]
    NMF[close_price[1:] < close_price[:-1]] = MF[close_price[1:] < close_price[:-1]]

    df = df[1:]
    df["PMF"] = PMF
    df["NMF"] = NMF

    for n in [14]:
        PMF_n = df["PMF"].rolling(n).sum()
        NMF_n = df["NMF"].rolling(n).sum()
        MR = PMF_n / NMF_n
        df["MFI_" + str(n)] = MR / (1 + MR)

    #df = df.reset_index()

    if (df["MFI_14"][-1] <= 0.3 or df["MFI_14"][-2] <= 0.3):
        print("under MFI 30 :", ticker)

    if ((df["MFI_14"][-1] >= 0.7 or df["MFI_14"][-2] >= 0.7) and ticker in buying_ticker):
        print("over MFI 70 :", ticker)

# 14일