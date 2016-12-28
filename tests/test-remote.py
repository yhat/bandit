import unittest
from bandit import Bandit

bandit = Bandit("glamp", "26daad20-cc45-11e6-9f6a-0242ac110003", "http://54.201.192.120/")

class TestBasic(unittest.TestCase):

    def test_can_run_job(self):
        self.assertEqual(bandit.run('ncaa-scraper'), "OK")

    def test_can_get_jobs(self):
        jobs = bandit.get_jobs()
        self.assertEqual(type(jobs), type([]))

    def test_can_get_job_results(self):
        results = bandit.get_job_results()
        self.assertEqual(type(results), type([]))

if __name__=="__main__":
    unittest.main()
