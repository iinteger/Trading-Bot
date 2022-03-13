# Trading-Bot

일확천금💸을 향한 가상화폐💰 봇 개발기💹

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

