#!/usr/bin/env python

import pandas as pd
from sklearn import datasets ## imports datasets from scikit-learn
data = datasets.load_boston() ## loads Boston dataset from datasets library

# define the data/predictors as the pre-set feature names  
df = pd.DataFrame(data.data, columns=data.feature_names)

# Put the target (housing value -- MEDV) in another DataFrame
target = pd.DataFrame(data.target, columns=["MEDV"])

X = df
y = target["MEDV"]


#And then fit a model:
from sklearn import linear_model
lm = linear_model.LinearRegression()
#lm = linear_model.LinearRegression(fit_intercept=True)
model = lm.fit(X,y)

print model.coef_.sum()+model.intercept_
print model.predict([[1,1,1,1,1,1,1,1,1,1,1,1,1]])[0]


predictions = model.predict(X)
print(predictions)[0:5]

print(model.coef_)
