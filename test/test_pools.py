
from lrbd import Pools
import unittest
import re, tempfile

class PoolsTestCase(unittest.TestCase):

    def setUp(self):
        self.p = Pools()
        self.p.add("swimming")

    def test_add(self):
        assert self.p.pools[0]['pool'] == "swimming"

    def test_append(self):
        data = { 'gateways': [] }
        self.p.append("swimming", data)
        self.p.display()
        assert self.p.pools[0]['pool'] == "swimming"



