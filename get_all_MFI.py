import pybithumb
import numpy as np
import pandas as pd
import warnings
from tqdm import tqdm
warnings.filterwarnings("ignore")

# BTC ETH ADA
tickers = pybithumb.get_tickers()
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
        print(ticker)

df.drop(["open", "high", "low", "volume", "time"], inplace=True, axis=1)

result = pd.DataFrame()
for n in [5, 10, 14, 20]:
    record = []
    mfi_data = df
    MFI = mfi_data["MFI_" + str(n)].values

    buy_point_list = (MFI[1:] < 0.3) & (MFI[:-1] >= 0.3)
    buy_point_list = np.insert(buy_point_list, 0, False)
    buy_point_list = mfi_data.index[buy_point_list]
    sell_point_list = (MFI[1:] >= 0.7) & (MFI[:-1] < 0.7)
    sell_point_list = np.insert(sell_point_list, 0, False)
    sell_point_list = mfi_data.index[sell_point_list]

    for bp in buy_point_list:
        if (sum(bp < sell_point_list) > 0) and (bp + 1 <= mfi_data.index[-1]):
            buy_price = mfi_data.loc[bp + 1, "close"]
            sp = sell_point_list[sell_point_list > bp][0] + 1
            if sp <= mfi_data.index[-1]:
                sell_price = mfi_data.loc[sp, "close"]
                profit = (sell_price - buy_price) / buy_price * 100
                record.append(profit)
        else:
            break

    result = pd.concat([result, pd.Series(record).describe()], axis = 1)

result.columns = [5, 10, 14, 20]
print(result)
# 14일