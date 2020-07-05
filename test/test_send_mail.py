# Imports TestCase class of unittest library
from unittest import TestCase

# Imports SendMail class
from ikk.send_mail import SendMail

# Tests whether an STMP connection can be set up using the parameters in config.py
# If this fails the user probably did not enter his credentials right
class TestSendMail(TestCase):

    # Sets up mail instance
    def setUp(self):
        self.mail_instance = SendMail()

    # Tests connection using function test_connection in send_mail.py
    # Does not send actual emails
    def test_test_connection(self):
        self.assertTrue(self.mail_instance.test_connection())
