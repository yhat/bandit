import unittest
from bandit import Bandit
import os


class TestBasic(unittest.TestCase):

    def test_send_many(self):
        os.environ['DATABASE_theoreticalDB'] = 'hello'
        bandit = Bandit()
        connection = bandit.get_connection('theoreticalDB')
        self.assertEqual('hello', connection)

if __name__=="__main__":
    unittest.main()
