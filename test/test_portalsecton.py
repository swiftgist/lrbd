
from lrbd import *
import unittest
#import re, tempfile

class PortalSectionTestCase(unittest.TestCase):

    def setUp(self):
        self.pt = PortalSection()
        data = [ { "name": "portal1", "addresses": [ "172.16.1.16" ] } ]
        self.pt.add(data)

    def test_add(self):
        self.pt.display()
        assert self.pt.portals[0]['name'] == "portal1"

    def test_purge(self):
        self.pt.purge("portal2")
        self.pt.display()
        assert not self.pt.portals



