import unittest
from bandit import Bandit

bandit = Bandit("glamp", "fe69f312-cb65-11e6-9d5f-6c400889bca4", "http://localhost:4567/")

class TestBasic(unittest.TestCase):

    # def test_can_run_job(self):
    #    self.assertEqual(bandit.run('ncaa-scraper'), "OK")

    def test_can_get_jobs(self):
        jobs = bandit.get_jobs()
        self.assertEqual(type(jobs), type([]))

    def test_can_get_job_results(self):
        results = bandit.get_job_results()
        self.assertEqual(type(results), type([]))

    def test_add_metadata(self):
        bandit.metadata.one = 1
        bandit.metadata.two = 2
        bandit.metadata.three = 3
        self.assertEqual(bandit.metadata, {"one": 1, "two": 2, "three": 3})

    def test_report_stuff(self):
        output = {'status': 'OK', 'message': 'DRY RUN'}
        self.assertEqual(bandit.report("ze-tag", 1, 2), output)

if __name__=="__main__":
    unittest.main()
