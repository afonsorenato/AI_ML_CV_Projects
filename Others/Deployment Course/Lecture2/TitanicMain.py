import re
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

pd.pandas.set_option('display.max_columns', None)

# Prepare dataset
data = pd.read_csv('https://www.openml.org/data/get_csv/16826755/phpMYEkMl')

# Data processing
data = data.replace('?', np.nan)

def get_first_cabin(row):
    try:
        return row.split()[0]
    except:
        return np.nan

data['cabin'] = data['cabin'].apply(get_first_cabin)

def get_title(passenger):
    line = passenger
    if re.search("Mrs", line):
        return "Mrs"
    elif re.search("Mr", line):
        return "Mr"
    elif re.search("Miss", line):
        return "Miss"
    else:
        return "Other"

data['title'] = data['name'].apply(get_title)
data['age'] = data['age'].astype('float')

data.drop(labels=['name', 'ticket', 'boat', 'body', 'home.dest'],
          axis=1, inplace = True)


data.to_csv('titanic.csv', index=False)

# Numerical and categorical variables
target = 'survived'
vars_num = [c for c in data.columns if data[c].dtypes!='O' and c!=target]
vars_cat = [c for c in data.columns if data[c].dtypes=='O']

print('Number of numerical variables: {}'.format(len(vars_num)))
print('Number of categorical variables: {}'.format(len(vars_cat)))

data[vars_cat].isnull().mean()
data[vars_cat].nunique()
data[vars_num].hist(bins=30, figsize=(10,10))
plt.show()

X_train, X_test, y_train, y_test = train_test_split(
    data.drop('survived', axis=1),  # predictors
    data['survived'],  # target
    test_size=0.2,  # percentage of obs in test set
    random_state=0)  # seed to ensure reproducibility

X_train['cabin'] = X_train['cabin'].str[0] # captures the first letter
X_test['cabin'] = X_test['cabin'].str[0] # captures the first letter

for var in ['age', 'fare']:

    # add missing indicator
    X_train[var+'_NA'] = np.where(X_train[var].isnull(), 1, 0)
    X_test[var+'_NA'] = np.where(X_test[var].isnull(), 1, 0)

    # replace NaN by median
    median_val = X_train[var].median()

    X_train[var].fillna(median_val, inplace=True)
    X_test[var].fillna(median_val, inplace=True)

X_train[vars_cat] = X_train[vars_cat].fillna('Missing')
X_test[vars_cat] = X_test[vars_cat].fillna('Missing')


def find_frequent_labels(df, var, rare_perc):
    # function finds the labels that are shared by more than
    # a certain % of the passengers in the dataset

    df = df.copy()

    tmp = df.groupby(var)[var].count() / len(df)

    return tmp[tmp > rare_perc].index


for var in vars_cat:
    # find the frequent categories
    frequent_ls = find_frequent_labels(X_train, var, 0.05)

    # replace rare categories by the string "Rare"
    X_train[var] = np.where(X_train[var].isin(
        frequent_ls), X_train[var], 'Rare')

    X_test[var] = np.where(X_test[var].isin(
        frequent_ls), X_test[var], 'Rare')

for var in vars_cat:
    # to create the binary variables, we use get_dummies from pandas

    X_train = pd.concat([X_train,
                         pd.get_dummies(X_train[var], prefix=var, drop_first=True)
                         ], axis=1)

    X_test = pd.concat([X_test,
                        pd.get_dummies(X_test[var], prefix=var, drop_first=True)
                        ], axis=1)

X_train.drop(labels=vars_cat, axis=1, inplace=True)
X_test.drop(labels=vars_cat, axis=1, inplace=True)

X_test['embarked_Rare'] = 0
variables = [c  for c in X_train.columns]

scaler = StandardScaler()

#  fit  the scaler to the train set
scaler.fit(X_train[variables])

# transform the train and test set
X_train = scaler.transform(X_train[variables])
X_test = scaler.transform(X_test[variables])

# set up the model
# remember to set the random_state / seed
model = LogisticRegression(C=0.0005, random_state=0)

# train the model
model.fit(X_train, y_train)

class_ = model.predict(X_train)
pred = model.predict_proba(X_train)[:,1]

# determine mse and rmse
print('train roc-auc: {}'.format(roc_auc_score(y_train, pred)))
print('train accuracy: {}'.format(accuracy_score(y_train, class_)))
print()

# make predictions for test set
class_ = model.predict(X_test)
pred = model.predict_proba(X_test)[:,1]

# determine mse and rmse
print('test roc-auc: {}'.format(roc_auc_score(y_test, pred)))
print('test accuracy: {}'.format(accuracy_score(y_test, class_)))
print()
