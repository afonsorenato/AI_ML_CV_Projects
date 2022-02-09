"""
1) Transformers
    Has two methods:
        fit()
        transform()
            scalers()
            feature selectors()
            Encoders()
            Discretizers()
2) Estimators
    Have two methods:
        fit()
        predict()
            Examples: Lasso, Decision Tree, SVMs, etc
3) Pipeline
    Has two methods:
        name_steps()
        final_estimator()

One hot encoding: representing categorical variables as binary vectors

Discretisation methods:
- Decision tree discretiser
"""


class MeanImputer:

    def __init__(self, variables):
        self.variables = variables

    def fit(self, x, y=None):
        self.imputer_dict_ = X[self.variables].mean().to_dict()

        return self


my_imputer = MeanImputer(variables=['age', 'fare'])

print(my_imputer.variables)
