# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('fish.csv', index_col=0)

dfana = df[df.fishname == "シコイワシ"]

pg = sns.pairplot(dfana)
print(type(pg))

#plt.matshow(df.corr())
#plt.show()