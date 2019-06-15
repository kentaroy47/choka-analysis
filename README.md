# choka-analysis
under development.

right now: 釣りビジョンの釣果をスクレイピング→可視化

goal: 釣果期待値が高い日を天気、気温などから予測できるように（したい。）

domain: 本牧海釣り公園。他の海釣り公園へ拡張予定。

## Requires python library:
BeautifulSoup

Pandas

seaborn

pipでインスコできます。

## スクレイピング
```
python scrape-test.py
```

## 解析・可視化
```
python analyze.py
# 可視化したい魚種をスクリプト中に記入。
```
