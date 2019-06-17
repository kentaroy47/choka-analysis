# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns

df = pd.read_csv('../seaborn-data/iris.csv', index_col=0)
# df = sns.load_dataset("iris")

pg = sns.pairplot(df)
print(type(pg))