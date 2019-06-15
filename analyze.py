# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('fish.csv', index_col=0)

# 元データを視る
# print(df)

# 解析したい魚種を入力
# ex. "アジ", "シコイワシ"など
dfana = df[df.fishname == "シコイワシ"]

# 相関をプロット
pg = sns.pairplot(dfana)
print(type(pg))

