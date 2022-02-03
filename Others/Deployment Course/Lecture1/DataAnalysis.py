import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

pd.pandas.set_option('display.max_columns', None)


def analyse_na_value(df, var):
    df = df.copy()
    df[var] = np.where(df[var].isnull(),1,0)
    tmp = df.groupby(var)['SalePrice'].agg(['mean', 'std'])
    tmp.plot(kind='barh', y="mean", legend=False,xerr='std', title="Sale Price", color = "green")
    tmp.show()


# Load dataset
data = pd.read_csv('train.csv')
print(data.shape)
data.head()

# histogram to evaluate target distribution
#np.log(data['SalePrice']).hist(bins=50, density=True)
#plt.xlabel("Number of houses")
#plt.xlabel('Sale price')
#plt.show()


cat_vars = [var for var in data.columns if data[var].dtype == 'O']
cat_vars = cat_vars + ['MSSubClass']
print(len(cat_vars))

num_vars = [var for var in data.columns if var not in cat_vars and var != 'SalePrice']
print(len(num_vars))

vars_with_na = [var for var in data.columns if data[var].isnull().sum()> 0]
data[vars_with_na].isnull().mean().sort_values(ascending=False)

cat_na = [var for var in cat_vars if var in vars_with_na]
num_na = [var for var in num_vars if var in vars_with_na]

year_vars = [var for var in num_vars if "Yr" in var or "Year" in var]

data.groupby('YrSold')['SalePrice'].median().plot()
plt.ylabel("Median house price")