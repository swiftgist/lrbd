
from lrbd import InitiatorSettings, Common, Runtime, entries
from nose.tools import  *
import unittest, mock
import re, tempfile

class InitiatorSettingsTestCase(unittest.TestCase):

    def setUp(self):
        Common.config['iqns'] = [ "iqn.xyz" ]
        Common.config['auth'] = [ { "host": "igw1",
                                    "authentication": "acls",
                                    "acls": [{
                                      "initiator": "iqn.abc",
                                      "attrib_nopin_timeout": "15"
                                    }]
                                  } ]
        Common.config['portals'] = [ { "name": "portal1",
                                     "addresses": [
                                         "172.16.1.16"
                                     ] } ]
        Common.config['pools'] = [
                { "pool": "rbd",
                  "gateways": [
                    { "host": "igw1", "tpg": [
                        { "image": "archive",
                          "initiator": "iqn.abc",
                          "portal": "portal1" }
                        ]
                    } ]
                } ]

        Runtime.config['addresses'] = [ "172.16.1.16" ]
        Runtime.config['portals'] = {}
        Runtime.config['portals']["iqn.xyz"] = {}
        Runtime.config['portals']["iqn.xyz"]["archive"] = {}
        Runtime.config['portals']["iqn.xyz"]["archive"]["portal1"] = "1"

    def test_assign(self):
        class mock_InitiatorSettings(InitiatorSettings):

            def _tidy(self, target, entries):
                self.target = target
                self.entries = entries

        self.a = mock_InitiatorSettings()
        self.a.assign()
        assert self.a.target == "iqn.xyz"
        assert self.a.entries == [{'initiator': 'iqn.abc', 'attrib_nopin_timeout': '15'}]

    def test_tidy(self):
        class mock_InitiatorSettings(InitiatorSettings):

            def _save(self, target, initiator, settings):
                self.target = target
                self.initiator = initiator
                self.settings = settings

        settings = [{'initiator': 'iqn.abc', 'attrib_nopin_timeout': '15'}]
        self.a = mock_InitiatorSettings()
        self.a._tidy("iqn.xyz", settings)

        assert self.a.target == "iqn.xyz"
        assert self.a.initiator == "iqn.abc"
        assert self.a.settings == {'attrib_nopin_timeout': '15'}

