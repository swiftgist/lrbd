
from lrbd import Luns, Common, Runtime, entries
import unittest, mock
import re, tempfile

class LunsTestCase(unittest.TestCase):

    def setUp(self):
        Common.config = {
            "iqns": [ "iqn.xyz" ],
            "pools": [
                { "pool": "rbd",
                  "gateways": [
                    { "host": "igw1", "tpg": [
                        { "image": "archive" }
                        ]
                    } ]
                } ] }

    def test_lun(self):
        class mock_Luns(Luns):

            def _find(self):
                pass

            def _cmd(self, target, tpg, address):
                self.called = " ".join([ target, str(tpg), address ])

        self.l = mock_Luns()
        assert self.l.called == "iqn.xyz 1 archive"

    @mock.patch('glob.glob')
    def test_find(self, mock_subproc_glob):
        mock_subproc_glob = []
        class mock_Luns(Luns):

            def _cmd(self, target, tpg, address):
                self.called = " ".join([ target, str(tpg), address ])

        self.l = mock_Luns()
        assert self.l.exists == {'iqn.xyz': {}}

    @mock.patch('glob.glob')
    def test_find_existing(self, mock_subproc_glob):

        class mock_Luns(Luns):

            def _cmd(self, target, tpg, address):
                self.called = " ".join([ target, str(tpg), address ])

        with tempfile.NamedTemporaryFile(suffix="._1_1_1_1_1_1_tmp") as tmpfile:
            tmpfile.write("/dev/rbd/rbd/archive\n")
            tmpfile.flush()
            mock_subproc_glob.return_value = [ tmpfile.name ]
            self.l = mock_Luns()
            assert self.l.exists == {'iqn.xyz': {'1': ['archive']}}


    def test_cmd_for_rbd(self):

        Runtime.config['backstore'] = "rbd"
        class mock_Luns(Luns):

            def _find(self):
                pass

        self.l = mock_Luns()
        assert self.l.cmds == [ ['targetcli', '/iscsi/iqn.xyz/tpg1/luns', 'create', '/backstores/rbd/archive'] ]



    @mock.patch('lrbd.popen')
    def test_create_nothing(self, mock_subproc_popen):

        class mock_Luns(Luns):

            def _find(self):
                pass

            def _cmd(self, target, tpg, address):
                self.called = " ".join([ target, str(tpg), address ])

            def disable_auto_add_mapped_luns(self):
                pass

        self.l = mock_Luns()
        mock_subproc_popen.return_value = []
        self.l.create()

        assert not mock_subproc_popen.called

    @mock.patch('lrbd.popen')
    def test_create(self, mock_subproc_popen):

        class mock_Luns(Luns):

            def _find(self):
                pass

            def disable_auto_add_mapped_luns(self):
                pass

        self.l = mock_Luns()
        mock_subproc_popen.return_value = []
        self.l.create()

        assert mock_subproc_popen.called

    

