#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt

enroll=pd.read_csv("./enrollment_forecast.csv")

enroll.columns=['year','roll','unem','hgrad','inc']

plt.title("year vs inc")
#plt.scatter(enroll.unem,enroll.year,color='yellow')
plt.scatter(enroll.unem,enroll.roll,color='red')
#plt.scatter(enroll.unem,enroll.hgrad,color='green')
#plt.scatter(enroll.unem,enroll.inc,color='blue')
plt.show()
plt.clf()







