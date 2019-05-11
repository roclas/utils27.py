#!/usr/bin/env python

import pandas as pd


enroll=pd.read_csv("./enrollment_forecast.csv")
enroll.columns=['year','roll','unem','hgrad','inc']
print enroll.head()
print "\n--------------------------------------\n"
print enroll.corr()




import matplotlib.pyplot as plt
import seaborn as sns

corrmat = enroll.corr(method='spearman')
f, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corrmat, ax=ax, cmap="YlGnBu", linewidths=0.1)
plt.show()






