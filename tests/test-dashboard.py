from bandit import Bandit
from ggplot import mtcars

bandit = Bandit()
# print bandit.make_dashboard(table=mtcars.to_html(classes="table"))
# print bandit.make_dashboard(table=mtcars)
print bandit.make_dashboard(template_name='many-tables', tables=[mtcars.head().to_html(classes='table'), mtcars.tail().to_html(classes='table')])
