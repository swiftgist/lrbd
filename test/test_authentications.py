
from lrbd import Authentications, Common
import unittest
#import re, tempfile

class AuthenticationsTestCase(unittest.TestCase):

    def setUp(self):
        self.a = Authentications()
        self.data =  { "host": "igw1", "authentication": "tpg",
                       "tpg": { "userid": "common1", "password": "pass1" } }
        self.a.add(self.data)

    def test_add(self):
        self.a.display()
        assert self.a.authentications[0]['authentication'] == "tpg"

    def test_purge(self):
        Common.hostname = "igw2"
        self.a.purge()
        self.a.display()
        assert not self.a.authentications



