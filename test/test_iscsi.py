
from lrbd import entries, Iscsi, Common
import unittest
import mock

class IscsiTestCase(unittest.TestCase):

    def test_iscsi_default(self):
        Common.config = { "targets": [] }
        class mock_Iscsi(Iscsi):
            def _gen_wwn(self):
                pass
            def _assign_vendor(self):
                pass
        self.i = mock_Iscsi()
        print self.i.cmds
        assert self.i.cmds == [['targetcli', '/iscsi', 'create' ]]

    def test_iscsi_defined_target(self):
        Common.config = { "targets": [ { "host": "igw1", 
                                         "target": "iqn.xyz" } ] }
        class mock_Iscsi(Iscsi):
            def _gen_wwn(self):
                pass
            def _assign_vendor(self):
                pass

        self.i = mock_Iscsi()
        assert self.i.cmds == [['targetcli', '/iscsi', 'create', 'iqn.xyz' ]]

    @mock.patch('lrbd.popen')
    @mock.patch('glob.glob')
    def test_create_default(self, mock_subproc_popen, mock_subproc_glob):
        Common.config = { "targets": [ { "host": "igw1", 
                                         "target": "iqn.xyz" } ] }
        mock_subproc_glob.return_value = [ "/some/path/name" ]
        class mock_Iscsi(Iscsi):
            def _gen_wwn(self):
                pass
            def _assign_vendor(self):
                pass
        self.i = mock_Iscsi()
        self.i.create()
        assert (mock_subproc_popen.called and 
                Common.config['iqns'] == [ "iqn.xyz" ])

    @mock.patch('lrbd.popen')
    def test_create(self, mock_subproc_popen):
        Common.config = { "targets": [ { "host": "igw1", 
                                         "target": "iqn.xyz" } ] }
        class mock_Iscsi(Iscsi):
            def _gen_wwn(self):
                pass
            def _assign_vendor(self):
                pass
        self.i = mock_Iscsi()
        self.i.create()
        assert mock_subproc_popen.called


