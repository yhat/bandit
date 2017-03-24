### Getting Started

### Installation

`pip install -U bandit-cli`

## Setup the Auth

If you're running jobs on the Bandit server, you don't need to specify your
`USERNAME`, `APIKEY` or the `BANDIT_URL`, as they are environment variables.

```python
# Create an instance of the Bandit class:
bandit = Bandit()
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

## Stream Data

Stream data from jobs back to the Bandit UI

`bandit.stream(tag_name, y)`

__Parameters:__
- `tag_name` _(str)_: the name of value to be tracked
- `y` _(int, float)_: the y value

__Example:__

```python
for x in range(10):
    for y in range(10):
        bandit.stream('Chart Line Name', float(np.random.rand()))
        time.sleep(0.1)
```

## Saving files

Dealing with file paths on remote machines can be a bit confusing at times.

From the Bandit client, use `output_dir` to easily save / read files:

```python

df = pd.DataFrame({
  "A": [10,20,30,40,50],
  "B": [20, 30, 10, 40, 50],
  "C": [32, 234, 23, 23, 42523]
})

# save our data as a csv
df.to_csv(bandit.output_dir + 'mydata.csv')
```

## Customizing Emails

Send emails with a custom subject, body and attachments.

```python
# import the email class
email = Email()

# For running scripts locally you can add write_json=False
# email = Email(write_json=False)

# specify the body of the email
body = '''
    Below is the result of the successful nightly model training script \n
    \n
    Model Stats: \n
    - Model Formula: %s \n
    - Adj. R2: %s \n
''' % (str(result.model.formula), str(result.rsquared_adj))

email.body(body)

# set our subject line
today = datetime.date.today().strftime('%Y_%m_%d')
email.subject = '%s model results' % today

# Add our attachments
email.add_attachment(bandit.output_dir + 'datasample.csv')

# Send our email to Colin and Ron
email.send(['colin@yhathq.com', 'ron@channel4news.com'])
```
