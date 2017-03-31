from .job import Metadata
from .yhat_json import json_dumps
import requests
import pybars
import urlparse
import json
import time
import tempfile
import os
try:
    from pandas import DataFrame
except Exception as e:
    DataFrame = None


class Job(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.data = kwargs

    def __repr__(self):
        return "<Job {}/{}>".format(self.username, self.name)

class JobResult(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.data = kwargs

    def __repr__(self):
        return "<JobResult {}/{}/{}>".format(self.name, self.n, self.status)

class Bandit(object):
    """
    Client for communicating with the Bandit server.

    Parameters
    ==========
    username: str
        your Bandit (and also GitHub) username
    apikey: str
        your Bandit apikey
    url: str
        the url of your Bandit server (i.e. http://10.1.201.1/, http://bandit.yhat.com/)

    Examples
    ========
    >>> bandit = Bandit() # this will grab username, apikey, and url from environment variables
    >>> bandit = Bandit()
    """
    def __init__(self, username=None, apikey=None, url=None):
        self.username = os.environ.get('BANDIT_CLIENT_USERNAME', username)
        self.apikey = os.environ.get('BANDIT_CLIENT_APIKEY', apikey)
        self.url = os.environ.get('BANDIT_CLIENT_URL', url)

        self._is_local = False
        if self.username is None or self.apikey is None or self.url is None:
            self._is_local = True

        self.metadata = Metadata()

        if self._is_local==True:
            self.output_dir = tempfile.mkdtemp(prefix='tmp-bandit-')
        else:
            self.output_dir = '/job/output-files/'

    def run(self, project, jobname):
        """
        Run a job that's on Bandit

        Parameters
        ==========
        project: str
            the name of the project the job belongs to
        name: str
            the name of the job you'd like to run

        Examples
        ========
        >>> bandit = Bandit()
        >>> bandit.run("myproject", "my-first-job")
        OK
        """
        if self._is_local==True:
            print('/'.join([self.username, project, 'jobs', jobname]))
            return

        url = urlparse.urljoin(self.url, '/'.join(['api', 'projects', self.username, project, 'jobs', jobname]))
        r = requests.get(url, auth=(self.username, self.apikey))
        return r.json()

    def get_jobs(self):
        """
        Get a list of the jobs you have on Bandit

        Examples
        ========
        >>> bandit = Bandit()
        >>> bandit.get_jobs()
        """
        if self._is_local==True:
            print('/api/jobs')
            return

        url = urlparse.urljoin(self.url, '/api/jobs')
        r = requests.get(url, params={'format': 'json'}, auth=(self.username, self.apikey))
        jobs = r.json()['jobs']
        return [Job(**j) for j in jobs]

    def get_job_results(self):
        """
        Get a list of the job results from Bandit

        Examples
        ========
        >>> bandit = Bandit()
        >>> bandit.get_job_results()
        """
        if self._is_local==True:
            print('/api/job-results')
            return

        url = urlparse.urljoin(self.url, "/api/job-results")
        r = requests.get(url, params={'format': 'json'}, auth=(self.username, self.apikey))
        job_results = r.json()['jobResults']
        return [JobResult(**j) for j in job_results]

    def stream(self, tag_name, y):
        """
        Parameters
        ==========
        tag_name: str
            tag for the data point
        x: int, float
            x value for the data point
        y: int, float
            y value for the data point

        Examples
        ========
        >>> bandit = Bandit()
        >>> bandit.stream("thing", 10)
        >>> bandit.stream("thing", 20)
        >>> bandit.stream("thing", 30)
        """
        return self.report(tag_name, y)

    def report(self, tag_name, y):
        """
        Parameters
        ==========
        tag_name: str
            tag for the data point
        x: int, float
            x value for the data point
        y: int, float
            y value for the data point

        Examples
        ========
        >>> bandit = Bandit()
        >>> bandit.report("thing", 10)
        >>> bandit.report("thing", 20)
        >>> bandit.report("thing", 30)
        """

        if _is_numeric(y)==False:
            raise Exception("`y` parameter is not a number '{}'".format(y))

        data = dict(tag_name=tag_name.replace(' ', '-'), x=0, y=y)
        data = json.loads(json_dumps(data))

        # this is detecting whether or not this is being run on a bandit worker.
        # if we're not on a bandit worker, just do a "dry run"
        job_id = os.environ.get('BANDIT_JOB_ID')
        if not job_id or self._is_local==True:
            print(json_dumps(data))
            return { "status": "OK", "message": "DRY RUN" }

        # write/append to the charts.ndjson file that will be inside the container
        with open('/job/metadata/charts.ndjson', 'ab') as f:
            f.write(json_dumps(data) + '\n')

        url = urlparse.urljoin(self.url, '/'.join(['api', 'jobs', job_id, 'report']))
        r = requests.put(url, json=data, auth=(self.username, self.apikey))
        return r.json()

    def get_file(self, username, project, job, filename, n='latest'):
        """
        Fetch a file outputted by a job. This will return a string representation of the file.
        
        Parameters
        ==========
        username: str
            owner of the job
        project: str
            name of the project
        job: str
            name of the job
        filename: str
            name of the file
        n: str, int
            job # you'd like to retrieve the file for. defaults to latest.

        Examples
        ========
        >>> bandit = Bandit()
        >>> bandit.get_file('glamp', 'bandit-demos', 'deploy-to-ops', 'README.md')
        >>> bandit.get_file('glamp', 'bandit-demos', 'deploy-to-ops', 'classifier.pkl')
        """
        path = os.path.join('/api', 'projects', username, project, 'jobs', job, n, 'output-files', filename)
        url = urlparse.urljoin(self.url, path)
        r = requests.get(url, auth=(self.username, self.apikey))
        return r.text

    def get_connection(self, name):
        """
        Get a database connection string that's saved on Bandit

        Parameters
        ==========
        name: str
            name of the database connection

        Examples
        ========
        >>> bandit = Bandit()
        >>> bandit.get_connection('postgres-dw')
        # postgres://kermit:supersecretpass@productiondb.internal.hostname:5432/prod?ssl=true
        """
        return os.environ.get('DATABASE_' + name)

    def make_dashboard(self, name, template_file="raw-html.html", **kwargs):
        """
        Construct an HTML dashboard from Python objects. You can use one of the pre-defined
        templates (see dashboards/) or create your own!

        Parameters
        ==========
        template_file: str
            path to the template you'd like to use 
        kwargs:
            variables you'd like to put into your template

        Examples
        ========
        >>> from ggplot import mtcars
        >>> bandit = Bandit()
        >>> print bandit.make_dashboard("my dashboard", table=mtcars.to_html(classes="table"))
        >>> print bandit.make_dashboard("my dashboard", table=mtcars)
        >>> bandit.make_dashboard("my dashboard", template_file='raw-html.html', tables=[mtcars.head().to_html(classes='table'), mtcars.tail().to_html(classes='table')])
        """
        variables = {}
        for key, value in kwargs.items():
            if isinstance(value, DataFrame):
                value = value.to_html(classes='table table-bordered')
            variables[key] = value

        compiler = pybars.Compiler()

    
        template_file = os.path.abspath(template_file)
        if not os.path.exists(template_file):
            this_dir = os.path.dirname(os.path.realpath(__file__))
            template_file = os.path.join(this_dir, 'dashboards', template_file)
            if not os.path.exists(template_file):
                raise Exception("Could not file template file: " + template_file)

        template_string = open(template_file, 'rb').read()
        template_string = _to_unicode(template_string)
        template = compiler.compile(template_string)
        html = template(variables)

        if isinstance(html, pybars._compiler.strlist):
            html = "".join(html)

        if self._is_local==True:
            print(html)
            return

        if not name.endswith('.html'):
            name += '.html'

        with open(self.output_dir + name, 'wb') as f:
            f.write(html)

def _to_unicode(s):
    "python2/3 compatible unicoder"
    try:
        return unicode(s)
    except Exception as e:
        return str(text, 'utf-8')

def _is_numeric(x):
    try:
        float(x)
        return True
    except:
        return False
