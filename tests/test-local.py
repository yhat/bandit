import unittest
from bandit import Bandit

bandit = Bandit("glamp", "9c9fc856-d398-11e6-b0dd-6c400889bca4", "http://localhost:4567/")

class TestBasic(unittest.TestCase):

    def test_can_run_job(self):
        response = bandit.run('bandit-demos', 'echo1')
        self.assertEqual(response['status'], "OK")

    def tests_run_and_wait(self):
        results = bandit.run_and_wait('bandit-demos', 'echo1')
        for result in results:
            self.assertEqual(result.status, 'success')

    def tests_run_chain(self):
        jobs = [
            {'project': 'bandit-demos', 'name': 'echo1'},
            {'project': 'bandit-demos', 'name': 'echo1'},
            {'project': 'bandit-demos', 'name': 'echo1'}
        ]
        result = bandit.run_series(jobs)
        self.assertEqual(result['status'], 'success')

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
