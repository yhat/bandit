### Getting Started

### Installation

`pip install -U bandit-cli`

## Setup the Auth

If you're running jobs on the Bandit server, you don't need to specify your
`USERNAME`, `APIKEY` or the `BANDIT_URL`, as they are environment variables.

However, for testing scripts locally, you'll need to include them:


```python
# Read the environment variables in from the shell:
bandit = Bandit(os.environ.get('BANDIT_CLIENT_USERNAME'), \
                os.environ.get('BANDIT_CLIENT_APIKEY'), \
                os.environ.get('BANDIT_CLIENT_URL'))
```

## Tracking Data

When jobs are run, Bandit will automatically track:

- Input files
- Output files
- Metadata (*optional*)

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

`bandit.report(tag_name, y)`

__Parameters:__
- `tag_name` _(str)_: the name of value to be tracked
- `y` _(int, float)_: the y value

__Example:__

```python
for x in range(10):
    for y in range(10):
        for tag in ["a", "b", "c", "d", "e", "f", "g"]:
            bandit.report(tag, np.random.rand())
        time.sleep(0.1)
```

## Customizing Emails

Send emails with a custom subject, body and attachments.

```python
# specify the body of the email
body = 'This is an email body'

email = job.Email(["colin@yhathq.com"])
email.subject("Email from Bandit")
email.body(body)
```
