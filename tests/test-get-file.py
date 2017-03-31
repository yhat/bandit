import unittest
from bandit import Bandit

bandit = Bandit()

class TestBasic(unittest.TestCase):

    def test_get_file(self):
        r = bandit.get_file('glamp', 'bandit-demos', 'deploy-to-ops', 'README.md')
        print(r)
        print(r.text)

if __name__=="__main__":
    unittest.main()
