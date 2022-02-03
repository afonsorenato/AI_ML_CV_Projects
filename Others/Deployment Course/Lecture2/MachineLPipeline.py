import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, r2_score

pd.pandas.set_option('display.max_columns', None)

x_train = pd.read_csv('xtrain.csv')
x_test = pd.read_csv('xtest.csv')

y_train = pd.read_csv('ytrain.csv')
y_test = pd.read_csv('ytest.csv')

# Load the selected features
features = pd.read_csv('selected_features.csv')
features = features['O'].to_list()

x_train = x_train[features]
x_test = x_test[features]

# Lasso regression
lin_model = Lasso(alpha=0.001, random_state = 0)
lin_model.fit(x_train, y_train)

# Evaluate the model
pred = lin_model.predict(x_train)

print(mean_squared_error(np.exp(y_train), np.exp(pred)))
print(mean_squared_error(np.exp(y_train), np.exp(pred)), squared=False)
print(r2_score(np.exp(y_train), np.exp(pred)))

plt.scatter(y_test, lin_model.predict(x_test))
plt.xlabel("True house price")
plt.ylabel('Predicted house price')
plt.title('Evaluate of Lasso Predictions')

# Save the model
joblib.dump(lin_model, 'linear_regression.joblib')