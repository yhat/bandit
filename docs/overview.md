## Getting Started

`pip install -U bandit-cli`

## Setup the Auth

```python
bandit = Bandit('<USERNAME>', '<API_KEY>','<BANDIT_URL>')
```

## Metadata

The Bandit CLI can be used to track metrics across different job runs.  For example
if we configure a job to train a regression model once a week, we can track the R²
and AIC values each time the job runs.

Below we train a simple linear regression and track `R2` and `AIC`

```python
from bandit import Bandit
import pandas as pd
import statsmodels.formula.api as sm

df = pd.DataFrame({"A": [10,20,30,40,50], "B": [20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})

result = sm.ols(formula="A ~ B + C", data=df).fit()

bandit.metadata.R2 = result.rsquared
bandit.metadata.AIC = result.aic
```
