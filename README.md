# Trading-Bot

가상화폐, 주식 봇 개발기

</br>

## 22. 01. 18 ~ 01. 22

* 변동성 돌파 전략을 사용하는 봇 제작
  
  * today_open + (yesterday_high - yesterday_low) * k (k = 0.8) 의 조건을 만족할 시 매수 -> 장 마감에 매도
  
  * 암호화폐 시장은 24시간이기 때문에 자정에 기준값 갱신, 매도

</br>

* 문제 :  거래시간이 6시간인 주식시장과 달리 암호화폐 거래는 24시간 내내 돌아감. 그래서 매수가 일찍 될 경우 자정에 매도가 되기 전에 가격이 떨어지는 문제가 있음
  
  * 개선 : 거래 시간을 12:00 ~ 24:00 으로 줄임

</br>

* 문제 : 거래 시간을 줄여도 동일한 문제가 생김. 그러나 거래 시간을 더 줄이면 24시간 활성화되어있는 암호화폐 거래의 장점이 사라질것으로 예상됨
  
  * 개선 : 장 마감시 매도를 하는것이 아니라, 목표 수익률을 잡고 가격이 도달하면 즉시 매도하는 방식으로 개선
  
  * 매수 가격으로부터 위, 아래로 3% 지점을 익절, 손절 가격으로 지정

</br>

* 어느정도 거래가 활성화되고, 수익이 발생하기도 함

</br>

* 문제 : 주문 명령이 모두 시장가 거래로 이루어짐. 시장가 거래를 하면 거래가 100%로 성사되지만 의도치 않은 슬리피지 비용이 많이 발생함. 특히 매도할 때, 목표가보다 훨씬 낯은 가격으로 매도되는 경우가 많았음

* 이때, 수익 3번과 손실 1번의 금액이 비슷했음
  
  * 개선 : 매도 주문을 지정가 주문으로 바꿈. 빗썸 API는 주문 금액을 호가 단위에 맞춰서 주문하지 않으면 에러를 리턴하기 때문에 주문시에 호가 단위를 맞추는 작업을 추가함
  
  * 더불어 익절을 4%에서, 손절을 -10%에서 하는것으로 수정. -3%에서 손절을 하는 경우, 주가가 진동하다가 손절되는 경우가 있었음

</br>

## 22. 01. 24

* 문제 : 손절매 지점이 너무 낮게 설정되어 손절매 시 손해금액이 너무 커짐
  
  * 개선 : 손절매 지점을 -5%로 수정

</br>

## 22. 01. 25

* 현재 알고리즘을 폐기하고 원래 알고리즘으로 복귀
- 문제 : 변동성 돌파 전략의 단점은 변동성이 큰 자산군(시총이 작은 종목)에서는 잘 먹히지 않는다는 점. 테스트에서 매수, 매도에 걸리는 종목은 대부분 시총이 작은 종목들이었고, 손해 비율이 더 컸음
  
  - 개선 : 장중 매수, 장 마감 매도인 원래 변동성 돌파 전략을 그대로 사용. 대신 종목을 시총 1, 2위인 비트코인과 이더리움으로 한정함. k값은 2020~2021년 백테스트 결과로 가장 좋았던 0.8, 0.7을 각 종목에 사용함

</br>

## 22. 01. 28

- ADA 종목 추가. 시총은 이전 두 종목에 비해 작지만 전체 암호화폐 시총 6위이며, 백테스트 결과 높은 ror과 상대적으로 낮은 mdd값을 보임

- 각 종목의 Range K 값 미세 조정. 변경할 K값은 21 ~ 22년 데이터의 백테스트로 결정
* 문제 : 자정에서 날짜가 바뀔 때 매개변수들도 모두 갱신하게 되는데, 날짜가 바뀐 직후 (10초 내외)에는 빗썸 데이터 갱신이 잘 이루어지지 않아서 이전날의 목표 가격을 그대로 가지고 가는 경우가 발생함
  
  * 개선 : 날짜가 바뀌면 매개변수를 즉시 갱신하지 않고, sleep(60)을 호출하여 빗썸 데이터 갱신을 기다린 후 매개변수를 갱신함

<div>
</br>
</div>

## 22. 02. 10

* **기존 알고리즘을 폐기하고 새 알고리즘으로 변경 (unlimit.py)**

* 변동성 돌파를 사용하지 않고 꾸준히 매수, 매도를 하며 지수를 추종하는 알고리즘

* 매수 알고리즘
  
  * 1시간에 한번씩 정기적으로 매수. 한번에 매수하는 금액은 15000원을 넘지 않고, 매수시점의 RSI 값에 따라서 3000 ~ 15000원 사이로 매수함
  
  * 현재 평단의 -n%가 될때마다 5000원씩 추가매수. 추가매수는 지정된 시간 없이 계속 감시되다가 포인트에 도달하면 바로 매수.  n은 현재 보유원화에 따라 바뀜

* 매도 알고리즘
  
  * 현재 평단의 +n%가 될때 전액 매도. 매도는 지정된 시간 없이 계속 감시되다가 포인트에 도달하면 바로 매도. n은 현재 보유원화에 따라 바뀜

* 변수는 보유원화가 줄어들수록 보수적으로 작동하게 설정

* 2.05 ~ 2. 10 테스트 결과, 3~5% 내외의 수익률 달성. 하락장이 끝난 후 상승장에서 큰 수익이 누적됨

<div>
</br/>
</div>

## 22. 02. 11

* 나스닥 폭락의 영향으로 암호화폐 시장지수도 하락. 특히 알트코인 위주로 폭락함

* 전체 종목에서 추매비용이 발생하였는데, 특히 200만원 이상으로 몸집이 커진 종목은 코스트 에버리징 능력이 떨어졌음. **종목당 최대 매수금액 제한이 필요할것같음**

* 현재 비트코인과 이더리움을 제외한 알트코인 9종목으로 테스트중인데, 높은 변동성으로 인해 시드머니가 마르는 경우가 생김. **변동성이 너무 큰 하위종목을 일정 배제하고 매매금액을 조정하는 방법으로 변동성을 낮추고 안정성을 높일 필요가 있음**

<div>
</br>
</div>

## 22. 02. 12

* 폭락의 영향으로 하방 빔(beam)이 나오며 시드가 붕괴됨. 개별 종목에 대한 헷지 수단은 있었지만, 여러 종목으로 돌렸기 때문에 무의미했음. 최종적으로 리플을 제외한 다른 종목은 트레이딩을 중단하고 손절

* 한 종목에 대해 구매할 수 있는 최대 금액을 설정하였고, 물타기 매매를 없앴음. 최종적으로 매수는 시간당 1번만 실행됨

* 라오어의 무한매수법 v2.1을 코인 트레이딩으로 구현함(unlimit v2.1.py)

<div>
</br>
</div>

## 22. 03. 13

* 주식 대상 갭 차이 수익률 시뮬레이션 구현 (Gap Earnings.ipynb)

<div>
</br>
</div>

## 22. 03. 29

- Quant-trading에서 다뤘던 MFI를 적용한 매매를 코인에 적용하여 구현 (get_all_MFI_.py)
- MFI 기준일은 빗썸 앱의 디폴트값은 14일로 설정
- 빗썸의 전체 종목에 적용한 결과, 평균값은 3.02, 중위수는 1.2로 긍정적임
- MFI_14가 30이하일때 매수하는 규칙에 따라 DAI, NPT 종목을 각 50000원씩 매수

<div>
</br>
</div>

## 22. 03. 30

* 미국 주식에서 특정 종목의 베타값을 구하는 코드 구현 (get_Beta.py)

<div>
</br>
</div>

## 22. 04. 08

- 3월 29일에 구매했던 DAI 종목의 MFI가 70을 돌파하여 매도
  - 구매금액 : 1206원
  - 판매금액 : 1235원
  - 수익률 : 2.3 % (1204원)
- RSI를 사용한 종목추천을 구현 (get_all_RSI.py)
- RSI나 MFI등의 보조지표를 사용하려면 종목의 거래량과 시가총액 등이 어느정도 규모가 있어야 할것같음. 너무 규모가 작은 종목은 가격의 변화가 지표와 독립적인 경우가 많음

<div>
</br>
</div>

## 22. 04. 27

- Logistic Regression을 사용하여 다음날의 상승, 하락 여부로 매매하는 알고리즘 구현. (Rogistic Regression.ipynb)
- 다양한 파라미터 조합으로 S&P를 상회하는 수익률을 달성
- 이동평균선같은 보조지표가 없을 때 오히려 더 높은 수익률을 달성함
- 또한 XGB를 사용했을때 변동성이 너무 커지는 영향이 있었음

<div>
</br>
</div>

## 22. 05. 04

- Logistic Regression 매매 고도화

- 다양한 보조지표와 모델의 그리드서치로 최적 조합 탐색중
  
  - 현재 최적 조합은 [시가, 종가, 시가-전날 종가, 시가-전날 시가] 데이터셋과 Linear Regression
  - 이때 테스트 정확도는 55.23%
  - 랜덤포레스트와 XGB에서 시장과 반대로 수익률이 진행되는 현상이 나타남
* TP와 FP의 비율이 비슷하고 TN과 FN의 비율이 비슷함. 즉 실제론 하락장인데 상승으로 예측하는 경우가 문제

* 하락 클래스의 Recall, F-1 Score를 높여야 할 필요가 있음
  
  * 미국시장이 장기적으로 상승하기 때문에 클래스당 데이터 갯수는 비슷하지만 상승으로 편향되는게 아닌가 하는 추측

<div>
</br>
</div>

## 22. 05. 27

- 배당주 투자를 위한 배당정보 크롤링 코드, 엑셀파일 추가 (stock info crawling.py)

<div>
</br>
</div>

## 22. 08. 03

- 볼린저 밴드를 활용한 매매전략을 구현 (bollinger band.ipynb)
  
  - 2시그마에 해당하는 하한선에 닿을 때 매수, 상한선에 닿을 때 매도
  - 하한선에 닿았음에도 계속 하락하는 경우가 생겼음. 이를 방지하기 위해 구매가에서 5% 이상 손실이 날 경우 손절하는 전략 추가. 수익률이 크게 상승함
  - QQQ 전체 구간에서 총 수익률 
* 전략을 적용했을 때 오늘 매수할 종목을 찾는 코드를 구현 (find tickers.ipynb)

* 테스트 결과 개별 주식보다는 지수 추종에서 더 높은 수익률을 보였고, 레버리지 ETF보다는 1배수 ETF에서 수익률이 극대화됐음. 이는 개별 종목에서 이벤트가 발생하면 급격하게 주가가 움직이는데 이러한 움직임이 정규분포에 해당하지 않아서 발생하는것으로 생각됨

* 테스트 수익률
  
  * SPY 2017-09-27 부터 바이앤홀드 : 77.11%, 볼린저밴드 전략 : 65%
  
  * QQQ 2017-09-27 부터 바이앤홀드 : 124.74%, 볼린저밴드 전략 : 115%

* 단순 바이앤홀드가 절대 수익은 더 높지만 본 전략은 여러 종목에 대해서 자금을 유동적으로 운영하며 수익률을 극대화하는데 의의가 있음

<div>
</br>
</div>

## 22. 08. 04

- 개별 종목 조회 시 시가총액이 너무 작은 종목은 제외하는 방안 고려중
- -20%에 가깝게 하락하는 등의 이슈가 있으면 현재 가격과 목표가, 손절가의 괴리가 심해지는 것을 발견

<div>
</br>
</div>

## 22. 08. 15

- 12일간 테스트 결과 전체 전체 수익률은 12.68%, 수익금은 10368원 달성
- 가장 큰 수익률은 10.3% (10371원) 이었고, 가장 큰 손해는 -9%(-47174원) 이었음. 예상하였듯 개별종목에서 가격이 급변하는 이벤트가 있었으며, 이는 매매 금액 조절을 통해 리스크를 관리하는 것이 중요하다는 것을 의미
- 기존 전략에 이평선과 밴드의 정배열, 역배열 여부에 따라 매수, 매도를 하는 방법을 구현. 수익률은 바이앤홀드와 유사한 수준으로 올랐으나 매매가 너무 잦아져 직접 매매에는 적합하지 않다고 판단. 이후 로보 어드바이저와 접목할 수 있을듯 함
- 볼린저 밴드, 모멘텀, 이동평균선, RSI, MACD를 사용하여 현재 주가의 매수-매도 점수를 매겨 사용하는 코드 구현(ta.ipynb). 보조지표 구현은 ta-lib 라이브러리 사용
- 매수, 매도 점수 설정에 따라 바이앤홀드를 상회하는 수익률이 나타나기도 하며, 매매가 너무 빈번하게 발생하지 않고 안정적인 수익구간을 잘 포착하는 장점이 있음

<div>
</br>
</div>

## 22. 08. 24

- 포트폴리오를 분석하는 코드 구현 (portfolio analyze.ipynb)
- 시장 대비 포트폴리오의 수익금, 수익률, MDD 를 비교함 (더 리치 포트폴리오 분석 참고)
- 리밸런싱 여부, 리밸런싱 실행 월, 초기 자금 및 종목별 비중 설정 가능

<div>
</br>
</div>

## 22. 08. 27

- ta.ipynb를 사용하여 구매시점인 종목을 찾는 코드 구현 (find tickers ta.ipynb)
- 클래스 기반으로 수정
