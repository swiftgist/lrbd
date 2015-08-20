
from lrbd import entries, TPGs, Common, Runtime
from nose.tools import  *
import tempfile
import unittest
import mock

class TPGsTestCase(unittest.TestCase):

    def setUp(self):
        Common.config = { 
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive" } 
                        ] 
                    } ] 
                } ] }


    @mock.patch('lrbd.addresses')
    def test_tpgs(self, mock_subproc_addresses):
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass


        self.t = mock_TPGs()
        assert ('addresses' in Runtime.config and
            'remote' in Runtime.config and
            'portals' in Runtime.config)

    def test_add_none(self):
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _check_portal(self):
                pass

        self.t = mock_TPGs()
        assert not self.t.cmds

    def test_add(self):
        Common.config = { 
            "iqns": [ "iqn.xyz" ],
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive", "portal": "portal1" } 
                        ] 
                    } ] 
                } ] }
        class mock_TPGs(TPGs):

            def _remote(self):
                pass

            def _check_portal(self, name):
                pass

        self.t = mock_TPGs()
        assert self.t.cmds

    def test_check_portal(self):
        Common.config['portals'] = [ { "name": "portal1" } ]
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

        self.t = mock_TPGs()
        assert self.t._check_portal("portal1") == None

    @raises(ValueError)
    def test_check_portal_undefined(self):
        Common.config['portals'] = [ { "name": "portal1" } ]
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

        self.t = mock_TPGs()
        self.t._check_portal("portal2")

    def test_remote(self):
        Common.config['portals'] = [ { "name": "portal1", 
                                       "addresses": [ "172.16.1.16" ] } ]
        class mock_TPGs(TPGs):

            def _add(self):
                pass

        self.t = mock_TPGs()
        self.t.portals["iqn.xyz"] = {}
        self.t.portals["iqn.xyz"]["portal1"] = 1
        self.t.remote["iqn.xyz"] = None
        self.t.tpg["iqn.xyz"] = 2
        self.t._remote()
        assert self.t.cmds == [['targetcli', '/iscsi/iqn.xyz', 'create 2']]

    @mock.patch('glob.glob')
    def test_cmd(self, mock_subproc_glob):
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

        self.t = mock_TPGs()
        mock_subproc_glob.return_value = []
        result = self.t._cmd("iqn.xyz", "2")
        assert result == ['targetcli', '/iscsi/iqn.xyz', 'create 2']

    @mock.patch('glob.glob')
    def test_cmd_returns_empty(self, mock_subproc_glob):
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

        self.t = mock_TPGs()
        mock_subproc_glob.return_value = "/some/path"
        result = self.t._cmd("iqn.xyz", "2")
        assert result == []

    @mock.patch('lrbd.popen')
    def test_create(self, mock_subproc_popen):
        class mock_TPGs(TPGs):

            def _add(self):
                pass

            def _remote(self):
                pass

        self.t = mock_TPGs()
        self.t.cmds = [ [ "echo", "hello" ] ]
        self.t.create()
        assert mock_subproc_popen.called





