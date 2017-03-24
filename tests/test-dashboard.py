from bandit import Bandit
from ggplot import *

p = ggplot(diamonds, aes(x='price')) + geom_density()
p.save('/tmp/plot.png')
bandit = Bandit()
# print bandit.make_dashboard(table=mtcars.to_html(classes="table"))
# print bandit.make_dashboard(table=mtcars)
# print(bandit.make_dashboard(
#     template_name='image-with-tables',
#     img='/tmp/plot.png',
#     tables=[mtcars.head().to_html(classes='table'), mtcars.tail().to_html(classes='table table-striped')])
#     )

print(bandit.make_dashboard(
    template_name='/Users/glamp/workspace/github.com/yhat/bandit/bandit-client/tests/custom-dash.html',
    images=['/tmp/plot.png', '/tmp/plot.png', '/tmp/plot.png', '/tmp/plot.png'],
    tables=[mtcars.head().to_html(classes='table'), mtcars.tail().to_html(classes='table table-striped')])
    )
