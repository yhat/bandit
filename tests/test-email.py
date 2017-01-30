import unittest
from bandit import Email


class TestBasic(unittest.TestCase):

    def test_blank_email(self):
        email = Email(write_json=False)
        self.assertTrue(isinstance(email._write(), dict))

    def test_subject(self):
        email = Email(write_json=False)
        email.subject('hi')
        self.assertTrue(email._write()['subject'], 'hi')
    
    def test_body(self):
        email = Email(write_json=False)
        email.body('hi')
        self.assertTrue(email._write()['subject'], 'hi')
    
    def test_send(self):
        email = Email(write_json=False)
        email.send("hi@test.com")
        self.assertTrue(email._write()['recipients'], ['hi@test.com'])
    
    def test_send_warning(self):
        email = Email(write_json=False)
        email.send("hi@test.com,foo@bar.com")
        self.assertTrue(email._write()['recipients'], ['hi@test.com', 'foo@bar.com'])
    
    def test_send_many(self):
        email = Email(write_json=False)
        email.send(["hi@test.com", "bye@test.com"])
        self.assertTrue(email._write()['recipients'], ['hi@test.com', 'bye@test.com'])

if __name__=="__main__":
    unittest.main()
