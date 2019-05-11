#!/usr/bin/env python

import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt

# define the data/predictors as the pre-set feature names  
data = pd.read_csv('./test_04.csv')
data = data[data.X <= 100]

df = pd.DataFrame(data, columns=['X','y'])

X = df.iloc[:,0:1]
y = df.iloc[:,1]

#And then fit a model:
#lm = linear_model.LinearRegression()
lm = linear_model.LinearRegression(fit_intercept=True)
model = lm.fit(X,y)

print "\n--coef---------------"
print(model.coef_)
print "\n--intercept---------------"
print(model.intercept_)

print "\n\n--prediction for 1"
print model.predict([[1]])[0]

#plt.plot([0, 100], [model.predict([[0]])[0], model.predict([[100]])[0]], 'k-', lw=2,color='blue')
plt.plot([0, 100], [0, model.coef_[0]*100]+model.intercept_, 'k-', lw=2,color='green')



plt.scatter(data.X,data.y,color='red')
plt.show()


