from .job import Metadata
import requests
import urlparse
import json
import os


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
    >>> bandit = Bandit("glamp", "6b3dff08-6ad8-4334-b37b-ad6162a0d4cf", "http://localhost:4567/")
    """
    def __init__(self, username=None, apikey=None, url=None):
        self.username = os.environ.get('BANDIT_CLIENT_USERNAME', username)
        self.apikey = os.environ.get('BANDIT_CLIENT_APIKEY', apikey)
        self.url = os.environ.get('BANDIT_CLIENT_URL', url)

        if self.username is None:
            raise Exception("`username` cannot be None. Please set via `BANDIT_CLIENT_USERNAME` environment variable or via Bandit() constructor.")
        if self.apikey is None:
            raise Exception("`apikey` cannot be None. Please set via `BANDIT_CLIENT_APKEY` environment variable or via Bandit() constructor.")
        if self.url is None:
            raise Exception("`url` cannot be None. Please set via `BANDIT_CLIENT_URL` environment variable or via Bandit() constructor.")

        self.metadata = Metadata()

    def run(self, jobname):
        """
        Run a job that's on Bandit

        Parameters
        ==========
        name: str
            the name of the job you'd like to run

        Examples
        ========
        >>> bandit = Bandit("glamp", "6b3dff08-6ad8-4334-b37b-ad6162a0d4cf", "http://localhost:4567/")
        >>> bandit.run("my-first-job")
        OK
        """
        url = urlparse.urljoin(self.url, '/'.join(['jobs', self.username, jobname, 'run']))
        r = requests.get(url, auth=(self.username, self.apikey))
        return r.text

    def get_jobs(self):
        """
        Get a list of the jobs you have on Bandit

        Examples
        ========
        >>> bandit = Bandit("glamp", "6b3dff08-6ad8-4334-b37b-ad6162a0d4cf", "http://localhost:4567/")
        >>> bandit.get_jobs()
        """
        url = urlparse.urljoin(self.url, 'jobs')
        r = requests.get(url, auth=(self.username, self.apikey))
        jobs = r.json()['jobs']
        return [Job(**j) for j in jobs]

    def get_job_results(self):
        """
        Get a list of the job results from Bandit

        Examples
        ========
        >>> bandit = Bandit("glamp", "6b3dff08-6ad8-4334-b37b-ad6162a0d4cf", "http://localhost:4567/")
        >>> bandit.get_job_results()
        """
        url = urlparse.urljoin(self.url, "job-results")
        r = requests.get(url, auth=(self.username, self.apikey))
        jobs = r.json()['jobs']
        return [JobResult(**j) for j in jobs]

    def report(self, tag_name, x, y):
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
        >>> bandit = Bandit("glamp", "6b3dff08-6ad8-4334-b37b-ad6162a0d4cf", "http://localhost:4567/")
        >>> bandit.report("thing", 1, 10)
        >>> bandit.report("thing", 2, 20)
        >>> bandit.report("thing", 3, 30)
        """

        data = dict(tag_name=tag_name, x=x, y=y)

        # this is detecting whether or not this is being run on a bandit worker.
        # if we're not on a bandit worker, just do a "dry run"
        job_id = os.environ.get('BANDIT_JOB_ID')
        if not job_id:
            print(data)
            return { "status": "OK", "message": "DRY RUN" }

        # write/append to the charts.ndjson file that will be inside the container
        with open('metadata/charts.ndjson', 'ab') as f:
            f.write(json.dumps(data) + '\n')

        url = urlparse.urljoin(self.url, '/'.join(['jobs', job_id, 'report']))
        r = requests.put(url, json=data, auth=(self.username, self.apikey))
        return r.json()

# bandit = Bandit("glamp", "26daad20-cc45-11e6-9f6a-0242ac110003", "http://54.201.192.120/")
# bandit = Bandit("glamp", "fe69f312-cb65-11e6-9d5f-6c400889bca4", "http://localhost:4567")
# print bandit.run("gregfoo2")
# print bandit.get_jobs()
# print bandit.get_job_results()
# bandit.email.body("HI")
# bandit.email.body("HI")
# print(bandit.email)
# bandit.job.set_status("failed")
# bandit.job.set_status("success")
# import json
# bandit.job.metadata('{"r2value": 0.98}')
# bandit.job.add_metadata_key("greg", 1)
