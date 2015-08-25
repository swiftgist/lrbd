
from lrbd import Acls, Common, Runtime, entries
from nose.tools import  *
import unittest, mock
import re, tempfile

class AclsTestCase(unittest.TestCase):

    def setUp(self):
        Common.config['iqns'] = [ "iqn.xyz" ]
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
        Runtime.config['portals']["iqn.xyz"]["portal1"] = "1"

    def test_acls(self):
        class mock_Acls(Acls):

            def _find(self):
                pass

            def _cmd(self, target, tpg, initiator):
                self.called = " ".join([ target, str(tpg), initiator ])

        self.a = mock_Acls()
        assert self.a.called == "iqn.xyz 1 iqn.abc"

    @raises(ValueError)
    def test_acls_exception(self):
        Common.config['pools'] = [
                { "pool": "rbd",
                  "gateways": [
                    { "host": "igw1", "tpg": [
                        { "image": "archive", 
                          "portal": "portal1" }
                        ]
                    } ]
                } ] 

        class mock_Acls(Acls):


            def _find(self):
                pass

            def _cmd(self, target, tpg, initiator):
                self.called = " ".join([ target, str(tpg), initiator ])

        self.a = mock_Acls()

    @mock.patch('glob.glob')
    def test_find(self, mock_subproc_glob):
        mock_subproc_glob.return_value = [ "/s/k/c/t/i/t/t_1/a/iqn.abc" ]

        class mock_Acls(Acls):

            def _cmd(self, target, tpg, initiator):
                self.called = " ".join([ target, str(tpg), initiator ])

        self.a = mock_Acls()
        assert self.a.exists == {'iqn.xyz': {'1': ['iqn.abc']}}

    @mock.patch('glob.glob')
    def test_find_does_nothing(self, mock_subproc_glob):

        mock_subproc_glob.return_value = [ ]

        class mock_Acls(Acls):

            def _cmd(self, target, tpg, initiator):
                self.called = " ".join([ target, str(tpg), initiator ])

        self.a = mock_Acls()
        assert not self.a.initiators

    def test_cmd(self):

        class mock_Acls(Acls):


            def _find(self):
                pass

        self.a = mock_Acls()
        assert self.a.cmds == [['targetcli', '/iscsi/iqn.xyz/tpg1/acls', 'create', 'iqn.abc']]

    @mock.patch('lrbd.popen')
    def test_create(self, mock_subproc_popen):

        Common.config['iqns'] = [ "iqn.xyz" ]
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
        Runtime.config['portals']["iqn.xyz"]["portal1"] = "1"


        class mock_Acls(Acls):

            def _find(self):
                pass

            def _cmd(self, target, tpg, initiator):
                self.called = " ".join([ target, str(tpg), initiator ])

        self.a = mock_Acls()
        self.a.cmds = [[ "echo", "hello" ]]
        self.a.create()
        assert mock_subproc_popen.called
