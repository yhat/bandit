from .job import Metadata
import requests
import urlparse
import json
import time
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
        >>> bandit = Bandit("glamp", "6b3dff08-6ad8-4334-b37b-ad6162a0d4cf", "http://localhost:4567/")
        >>> bandit.run("myproject", "my-first-job")
        OK
        """
        url = urlparse.urljoin(self.url, '/'.join(['api', 'projects', self.username, project, 'jobs', jobname]))
        r = requests.get(url, auth=(self.username, self.apikey))
        return r.json()

    def run_and_wait(self, project, jobname, timeout=60*5):
        """
        ...
        """
        run = self.run(project, jobname)
        resultId = run['resultId']

        start_time = time.time()

        while (time.time() - timeout) <= start_time:
            for result in self.get_job_results():
                if result._id==resultId:
                    if result.status in ['failed', 'success']:
                        return result
            time.sleep(2)

        raise Exception("Job timed out")

    def run_series(self, jobs, timeout=60*5):
        """
        ...
        """
        results = []
        for job in jobs:
            project = job['project']
            name = job['name']
            timeout = job.get('timeout', timeout)
            results.append(self.run_and_wait(project, name, timeout=timeout))
        return results

    def get_jobs(self):
        """
        Get a list of the jobs you have on Bandit

        Examples
        ========
        >>> bandit = Bandit("glamp", "6b3dff08-6ad8-4334-b37b-ad6162a0d4cf", "http://localhost:4567/")
        >>> bandit.get_jobs()
        """
        url = urlparse.urljoin(self.url, '/api/jobs')
        r = requests.get(url, params={'format': 'json'}, auth=(self.username, self.apikey))
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
        url = urlparse.urljoin(self.url, "/api/job-results")
        r = requests.get(url, params={'format': 'json'}, auth=(self.username, self.apikey))
        job_results = r.json()['jobResults']
        return [JobResult(**j) for j in job_results]

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
        >>> bandit = Bandit("glamp", "6b3dff08-6ad8-4334-b37b-ad6162a0d4cf", "http://localhost:4567/")
        >>> bandit.report("thing", 10)
        >>> bandit.report("thing", 20)
        >>> bandit.report("thing", 30)
        """

        data = dict(tag_name=tag_name.replace(' ', '-'), x=0, y=y)

        # this is detecting whether or not this is being run on a bandit worker.
        # if we're not on a bandit worker, just do a "dry run"
        job_id = os.environ.get('BANDIT_JOB_ID')
        if not job_id:
            print(json.dumps(data, indent=2))
            return { "status": "OK", "message": "DRY RUN" }

        # write/append to the charts.ndjson file that will be inside the container
        with open('/job/metadata/charts.ndjson', 'ab') as f:
            f.write(json.dumps(data) + '\n')

        url = urlparse.urljoin(self.url, '/'.join(['api', 'jobs', job_id, 'report']))
        r = requests.put(url, json=data, auth=(self.username, self.apikey))
        return r.json()
