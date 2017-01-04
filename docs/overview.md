## Getting Started

`pip install -U bandit-cli`

## Setup the Auth

```python
bandit = Bandit('<USERNAME>', '<API_KEY>','<BANDIT_URL>')
```
## Tracking Data

When jobs are run, Bandit will automatically track:
- Input files
- Output files

These can be any sort of file (png, jpeg, xlsx, etc).

## Metadata

`bandit.metadata` _type_ dict

__Usage:__

```python
bandit.metadata.AUC = .68
bandit.metadata['AIC'] = .88
```

The Bandit CLI can be used to track metrics across different job runs.  For example
if we configure a job to train a regression model once a week, we can track the R²
and AIC values each time the job runs.

__Example:__

Below we train a simple linear regression and track `R2` and `AIC`

```python
from bandit import Bandit
import pandas as pd
import statsmodels.formula.api as sm

df = pd.DataFrame({
  "A": [10,20,30,40,50],
  "B": [20, 30, 10, 40, 50],
  "C": [32, 234, 23, 23, 42523]
})

result = sm.ols(formula="A ~ B + C", data=df).fit()

# track our two values
bandit.metadata.R2 = result.rsquared
bandit.metadata.AIC = result.aic
```

## Reports

Stream data from jobs back to the Bandit UI

`bandit.report(tag_name, x, y)`

__Parameters:__
- `tag_name` _(str)_: the name of value to be tracked
- `x` _(int, float)_: the x value
- `y` _(int, float)_: the y value

__Example:__

```python
for x in range(10):
    for y in range(10):
        for tag in ["a", "b", "c", "d", "e", "f", "g"]:
            bandit.report(tag, y, np.random.rand())
        time.sleep(0.1)
```

## Customizing Emails

```python
bandit.email.subject()
bandit.email.body()
bandit.email.attachment()
```
