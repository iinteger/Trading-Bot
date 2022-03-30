import numpy as np
import pandas_datareader as web
import pandas as pd
import datetime

tickers_list = []
tickers_name = []

start_day = datetime.datetime.now()-datetime.timedelta(days=5*365)  # 5년치

market_index_close = web.DataReader("^GSPC", start=start_day, data_source='yahoo')["Adj Close"]
AAPL_close = web.DataReader("AAPL", start=start_day, data_source="yahoo")["Adj Close"]

tickers_list.append(market_index_close)
tickers_name.append("S&P")
tickers_list.append(AAPL_close)
tickers_name.append("AAPL")

print("before set length")
print(tickers_list[0].shape)
print(tickers_list[1].shape)

min_length = min([ticker.shape[0] for ticker in tickers_list])
tickers_list = [ticker[len(ticker)-min_length:] for ticker in tickers_list]

print("after set length")
print(tickers_list[0].shape)
print(tickers_list[1].shape)

# date column drop
tickers_list = [ticker.reset_index() for ticker in tickers_list]
tickers_list = [ticker.iloc[:, -1] for ticker in tickers_list]
tickers_df = pd.concat(tickers_list, axis=1)
tickers_df.columns = tickers_name

# 각 컬럼의 일간수익률 계산
returns = tickers_df[[tickers_name[0], tickers_name[1]]].pct_change()

# 일간수익률에 루트 250을 곱해서 연율화, 변동성 계산
vols = [0]*len(tickers_df)

for i, ticker in enumerate(tickers_name):
    vols[i] = returns[ticker].std() * np.sqrt(250)

# 종목 수익률의 공분산
covs = returns.cov()

var = returns[tickers_name[0]].var()

# 베타 계산
beta = covs.loc[tickers_name[0], tickers_name[1]] / var
print(f"계산된 {tickers_name[1]} Beta (5Y):", beta)
print(f"실제 {tickers_name[1]} Beta (5Y): 1.19")