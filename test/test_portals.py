
from lrbd import Portals, Common, Runtime
from nose.tools import  *
import unittest, mock
import re, tempfile

class PortalsTestCase(unittest.TestCase):

    def setUp(self):
        Common.config['iqns'] = [ "iqn.xyz" ]
        Common.config['portals'] = [ { "name": "portal1",
                                     "addresses": [
                                         "172.16.1.16"
                                     ] } ]
        Runtime.config['addresses'] = [ "172.16.1.16" ]
        Runtime.config['portals'] = {}
        Runtime.config['portals']["iqn.xyz"] = {}
        Runtime.config['portals']["iqn.xyz"]["portal1"] = "1"


    def test_portal_default(self):
        Common.config['iqns'] = [ "iqn.xyz" ]
        Common.config['portals'] = []
        class mock_Portals(Portals):

            called = False

            def _cmd(self, target, tpg, address):
                self.called = True

        self.pt = mock_Portals()
        assert self.pt.called

    def test_portal(self):

        class mock_Portals(Portals):


            def _entries(self):
                yield("iqn.xyz", "portal1", Common.config['portals'][0])

            def _cmd(self, target, tpg, address):
                self.called = " ".join([ target, tpg, address ])

        self.pt = mock_Portals()
        assert self.pt.called == "iqn.xyz 1 172.16.1.16"

    def test_portal_remote(self):
        Runtime.config['addresses'] = [ "172.16.1.17" ]

        class mock_Portals(Portals):


            def _entries(self):
                yield("iqn.xyz", "portal1", Common.config['portals'][0])

            def _cmd(self, target, tpg, address):
                self.called = " ".join([ target, tpg, address ])

        self.pt = mock_Portals()
        assert self.pt.called == "iqn.xyz 2 172.16.1.16"


    def test_entries(self):

        class mock_Portals(Portals):

            def _cmd(self, target, tpg, address):
                self.called = " ".join([ target, tpg, address ])

        self.pt = mock_Portals()
        assert self.pt.called == "iqn.xyz 1 172.16.1.16"

    @raises(ValueError)
    def test_entries_exception(self):
        del Common.config
        Common.config = {}
        Common.config['iqns'] = [ "iqn.xyz" ]
        Common.config['portals'] = [ { "name": "portal99" } ]

        class mock_Portals(Portals):

            def _cmd(self, target, tpg, address):
                self.called = " ".join([ target, tpg, address ])

        self.pt = mock_Portals()


    @mock.patch('glob.glob')
    def test_portal_remote(self, mock_subproc_glob):
        Runtime.config['addresses'] = [ "172.16.1.17" ]

        mock_subproc_glob.return_value = []

        self.pt = Portals()
        assert self.pt.cmds == [['targetcli', '/iscsi/iqn.xyz/tpg2/portals', 'create', '172.16.1.16']]

    @mock.patch('glob.glob')
    def test_portal_remote_does_nothing(self, mock_subproc_glob):
        Runtime.config['addresses'] = [ "172.16.1.17" ]

        mock_subproc_glob.return_value = [ "/some/path" ]

        self.pt = Portals()
        assert self.pt.cmds == []

    @mock.patch('lrbd.popen')
    def test_create(self, mock_subproc_popen):
        Runtime.config['addresses'] = [ "172.16.1.17" ]
        Runtime.config['portals'] = {}
        Runtime.config['portals']["iqn.xyz"] = {}
        Runtime.config['portals']["iqn.xyz"]["portal1"] = "1"

        mock_subproc_popen.return_value = []

        self.pt = Portals()
        self.pt.create()
        assert mock_subproc_popen.called


