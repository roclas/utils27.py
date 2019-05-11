#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import scale
from collections import Counter


address="./enrollment_forecast.csv"
enroll=pd.read_csv(address)

enroll.columns=['year','roll','unem','hgrad','inc']
print enroll.head()
print enroll.corr()

#plt.scatter(enroll.unem,enroll.year,color='yellow')
plt.scatter(enroll.unem,enroll.roll,color='red')
#plt.scatter(enroll.unem,enroll.hgrad,color='green')
#plt.scatter(enroll.unem,enroll.inc,color='blue')
plt.show()
plt.clf()

plt.scatter(enroll.roll,enroll.year,color='yellow')
plt.scatter(enroll.roll,enroll.unem,color='red')
plt.scatter(enroll.roll,enroll.hgrad,color='green')
plt.scatter(enroll.roll,enroll.inc,color='blue')
plt.show()
plt.clf()
plt.scatter(enroll.year,enroll.inc,color='blue')
plt.title("year vs inc")
plt.show()
plt.clf()






