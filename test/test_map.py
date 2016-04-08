
from lrbd import Map, Common, Runtime, entries
from nose.tools import  *
import unittest, mock
import re, tempfile

class MapTestCase(unittest.TestCase):

    def setUp(self):
        Common.config = {
            "iqns": [ "iqn.xyz" ],
            "auth": [ { "host": "igw1", "authentication": "acls" } ],
            "pools": [
                { "pool": "rbd",
                  "gateways": [
                    { "host": "igw1", "tpg": [
                        { "image": "archive", "initiator": "iqn.abc" }
                        ]
                    } ]
                } ] }

    def test_map(self):

        class mock_Map(Map):

            def _lun(self, target, tpg, image):
                return("1")

            def _check(self, target, tpg, initiator):
                pass

            def _cmd(self, target, tpg, initiator, lun):
                self.called = " ".join([ target, str(tpg), initiator, lun ])

        self.m = mock_Map()
        assert self.m.called == "iqn.xyz 1 iqn.abc 1"

    # Something is seriously wrong with the patching... seems to be applied
    # to both return values.  The result does test the success condition.
    @mock.patch('os.path.basename')
    @mock.patch('glob.glob')
    def test_lun(self, mock_os_path_basename, mock_subproc_glob):

        #mock_subproc_glob.return_value = 
        mock_os_path_basename.return_value =  [ "/s/k/c/t/i/i/t/l/lun_0/rbd-archive" ]
                 
        class mock_Map(Map):

            def _cmd(self, target, tpg, initiator, lun):
                self.called = " ".join([ target, str(tpg), initiator, lun ])


        self.m = mock_Map()
        assert self.m.called == "iqn.xyz 1 iqn.abc rbd-archive"

    @raises(ValueError)
    @mock.patch('glob.glob')
    def test_lun_exception(self, mock_subproc_glob):

        mock_subproc_glob.return_value = []
                 
        class mock_Map(Map):

            def _cmd(self, target, tpg, initiator, lun):
                self.called = " ".join([ target, str(tpg), initiator, lun ])

        self.m = mock_Map()

    @mock.patch('glob.glob')
    def test_check(self, mock_subproc_glob):

        mock_subproc_glob.return_value = [ "/some/path" ]
        class mock_Map(Map):

            def _lun(self, target, tpg, image):
                return("1")

            def _cmd(self, target, tpg, initiator, lun):
                self.called = " ".join([ target, str(tpg), initiator, lun ])

        self.m = mock_Map()
        assert self.m.called == "iqn.xyz 1 iqn.abc 1"

    @raises(ValueError)
    @mock.patch('glob.glob')
    def test_check_exception(self, mock_subproc_glob):

        mock_subproc_glob.return_value = []
        class mock_Map(Map):

            def _lun(self, target, tpg, image):
                return("1")

            def _cmd(self, target, tpg, initiator, lun):
                self.called = " ".join([ target, str(tpg), initiator, lun ])

        self.m = mock_Map()

    @mock.patch('glob.glob')
    def test_cmd(self, mock_subproc_glob):

        mock_subproc_glob.return_value = [ ]
        class mock_Map(Map):

            def _lun(self, target, tpg, image):
                return("1")

            def _check(self, target, tpg, initiator):
                pass

        self.m = mock_Map()
        assert self.m.cmds == [['targetcli', '/iscsi/iqn.xyz/tpg1/acls/iqn.abc', 'create', '1', '1']]

    @mock.patch('glob.glob')
    def test_cmd_does_nothing(self, mock_subproc_glob):

        mock_subproc_glob.return_value = [ "/some/path" ]
        class mock_Map(Map):

            def _lun(self, target, tpg, image):
                return("1")

            def _check(self, target, tpg, initiator):
                pass

        self.m = mock_Map()
        assert not self.m.cmds

    @mock.patch('lrbd.popen')
    def test_map(self, mock_subproc_glob):

        class mock_Map(Map):

            def _lun(self, target, tpg, image):
                return("1")

            def _check(self, target, tpg, initiator):
                pass

            def _cmd(self, target, tpg, initiator, lun):
                self.called = " ".join([ target, str(tpg), initiator, lun ])

        self.m = mock_Map()
        self.m.cmds = [ [ "echo", "hello" ] ]
        self.m.map()
        assert mock_subproc_glob.called

    @mock.patch('lrbd.popen')
    def test_map_does_nothing(self, mock_subproc_glob):

        class mock_Map(Map):

            def _lun(self, target, tpg, image):
                return("1")

            def _check(self, target, tpg, initiator):
                pass

            def _cmd(self, target, tpg, initiator, lun):
                self.called = " ".join([ target, str(tpg), initiator, lun ])

        self.m = mock_Map()
        self.m.map()
        assert not mock_subproc_glob.called
