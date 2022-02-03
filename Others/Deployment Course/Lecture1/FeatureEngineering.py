import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

pd.pandas.set_option('display.max_columns', None)


def elapsed_years(df, var):
    df[var] = df['YrSold'] - df[var]
    return df

# Load dataset
data = pd.read_csv('train.csv')
data.head()

# Divide dataset
x_train, x_test, y_train, y_test = train_test_split(
    data.drop(['Id', 'SalePrice'], axis=1),
    data['SalePrice'],
    test_size=0.1, random_state=0, )

print(x_train.shape, x_test.shape)

y_train = np.log(y_train)
y_test = np.log(y_test)

cat_vars = [var for var in data.columns if data[var].dtype == 'O']
cat_vars = cat_vars + ['MSSubClass']

x_train[cat_vars] = x_train[cat_vars].astype('O')
x_test[cat_vars] = x_test[cat_vars].astype('O')

cat_vars_with_na = [
    var for var in cat_vars
    if x_train[var].isnull().sum() > 0]

x_train[cat_vars_with_na].isnull().mean().sort_values(ascending=False)

with_string_missing = [
    var for var in cat_vars_with_na if x_train[var].isnull().mean() > 0.1]

with_frequent_category = [
    var for var in cat_vars_with_na if x_train[var].isnull().mean() < 0.1]

x_train[with_string_missing] = x_train[with_string_missing].fillna('Missing')
x_test[with_string_missing] = x_test[with_string_missing].fillna('Missing')

for var in with_frequent_category:
    mode = x_train[var].mode()[0]
    print(var, mode)

    x_train[var].fillna(mode, inplace=True)
    x_test[var].fillna(mode, inplace=True)

num_vars = [var for var in data.columns
            if var not in cat_vars and var != 'SalePrice']
vars_with_na = [var for var in data.columns
                if data[var].isnull().sum() > 0]

for var in vars_with_na:
    mean_val = x_train[var].mean()

    x_train[var + '_na'] = np.where(x_train[var].isnull(), 1, 0)
    x_test[var + '_na'] = np.where(x_test[var].isnull(), 1, 0)

    x_train[var].fillna(mean_val, inplace=True)
    x_test[var].fillna(mean_val, inplace=True)

for var in ['YearBuilt', 'YearRemodAdd', 'GarageYrBlt']:
    x_train = elapsed_years(x_train, var)
    x_test = elapsed_years(x_test, var)

x_train.drop(['YrSold'], axis=1, inplace=True)
x_test.drop(['YrSold'], axis=1, inplace=True)