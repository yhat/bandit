import job
import requests


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
    def __init__(self, username, apikey, url):
        self.username = username
        self.apikey = apikey
        self.url = url
        self.job = job
        self.email = job.Email()

    def run(self, jobname):
        r = requests.get(self.url + "/jobs/" + self.username + "/" + jobname + "/run", auth=(self.username, self.apikey))
        return r.text

    def get_jobs(self):
        r = requests.get(self.url + "/jobs", auth=(self.username, self.apikey))
        jobs = r.json()['jobs']
        return [Job(**j) for j in jobs]

    def get_job_results(self):
        r = requests.get(self.url + "/job-results", auth=(self.username, self.apikey))
        jobs = r.json()['jobs']
        return [JobResult(**j) for j in jobs]


# bandit = Bandit("glamp", "26daad20-cc45-11e6-9f6a-0242ac110003", "http://54.201.192.120/")
bandit = Bandit("glamp", "fe69f312-cb65-11e6-9d5f-6c400889bca4", "http://localhost:4567")
print bandit.run("gregfoo2")
print bandit.get_jobs()
print bandit.get_job_results()
# bandit.email.body("HI")
# bandit.email.body("HI")
# print(bandit.email)
# bandit.job.set_status("failed")
# bandit.job.set_status("success")
# import json
# bandit.job.metadata('{"r2value": 0.98}')
# bandit.job.add_metadata_key("greg", 1)
