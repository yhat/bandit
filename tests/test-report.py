import unittest
from bandit import Bandit
import numpy as np
import random

bandit = Bandit("glamp", "9c9fc856-d398-11e6-b0dd-6c400889bca4", "http://localhost:4567/")

class TestBasic(unittest.TestCase):

    def test_report_int(self):
        output = {'status': 'OK', 'message': 'DRY RUN'}
        result = bandit.report("ze-tag", 1)
        self.assertEqual(result, output)

    def test_report_float(self):
        output = {'status': 'OK', 'message': 'DRY RUN'}
        result = bandit.report("ze-tag", random.normalvariate(0, 1))
        self.assertEqual(result, output)

    def test_report_numpy(self):
        output = {'status': 'OK', 'message': 'DRY RUN'}
        result = bandit.report("ze-tag", np.random.normal(0, 1))
        self.assertEqual(result, output)

if __name__=="__main__":
    unittest.main()
