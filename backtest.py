import pybithumb
import numpy as np
import pandas as pd

# BTC ETH ADA
df = pybithumb.get_ohlcv("ADA")
df = pd.concat([df["2021"], df["2022"]], axis=0)

maxvalue = 0
maxindex = 0
mdd = 0

for i in range(1, 100):
    df["ma5"] = df["close"].rolling(window=5).mean().shift(1)
    df["range"] = (df["high"] - df["low"]) * (i/100)
    # 목표가는 거래일 전날의 레인지를 사용하기 때문에 range를 하나씩 내려서 계산함
    df["target"] = df["open"] + df["range"].shift(1)
    df["bull"] = df["open"] > df["ma5"]

    fee = 0.0016
    df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)

    df["hpr"] = df["ror"].cumprod()
    df["dd"] = (df["hpr"].cummax() - df["hpr"]) / df["hpr"].cummax()*100

    mdd = df["dd"].max()
    ror = df["ror"].cumprod()[-2]
    if ror > maxvalue:
        maxvalue = ror
        maxindex = i/100
        mdd = mdd

print("max ror :", maxvalue)
print("mdd :", mdd)
print("threshold :", maxindex)

'''
df["range"] = (df["high"] - df["low"]) * (0.8)
# 목표가는 거래일 전날의 레인지를 사용하기 때문에 range를 하나씩 내려서 계산함
df["target"] = df["open"] + df["range"].shift(1)

fee = 0.0032
df["ror"] = np.where(df["high"] > df["target"], df["close"]/df["target"]-fee, 1)

ror = df["ror"].cumprod()[-2]
print(ror)
df.to_excel("btc.xlsx")
'''