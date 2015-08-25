
from lrbd import entries, Backstores, Common, Runtime
import os
import shutil
import tempfile
import unittest
import mock

class BackstoresTestCase(unittest.TestCase):

    def test_backstores_default(self):
        class mock_Backstores(Backstores):

            def _load_modules(self):
                pass

            def _rbd(self):
                pass

            def _iblock(self):
                pass

        self.b = mock_Backstores(None)
        assert Runtime.config['backstore'] == "rbd"

    def test_backstores_iblock(self):
        class mock_Backstores(Backstores):

            def _load_modules(self):
                pass

            def _rbd(self):
                pass

            def _iblock(self):
                pass

        self.b = mock_Backstores("iblock")
        assert Runtime.config['backstore'] == "iblock"

    def test_backstores_rbd(self):
        class mock_Backstores(Backstores):

            def _load_modules(self):
                pass

            def _rbd(self):
                pass

            def _iblock(self):
                pass

        self.b = mock_Backstores("rbd")
        assert Runtime.config['backstore'] == "rbd"


    def test_iblock(self):

        Common.config = { 
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive" } 
                        ] 
                    } ] 
                } ] }

        self.b = Backstores("iblock")
        assert self.b.cmds == [['targetcli', '/backstores/iblock', 'create', 'name=archive', 'dev=/dev/rbd/rbd/archive']]

    @mock.patch('glob.glob')
    def test_iblock_does_nothing(self, mock_subproc_glob):
        Common.config = { 
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive" } 
                        ] 
                    } ] 
                } ] }

        mock_subproc_glob.return_value = "globbed/path/name"
        self.b = Backstores("iblock")
        assert not self.b.cmds

    @mock.patch('glob.glob')
    def test_detect_default(self, mock_subproc_glob):
        Common.config = { 
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive" } 
                        ] 
                    } ] 
                } ] }
        class mock_Backstores(Backstores):
              def _load_modules(self):
                  pass

        mock_subproc_glob.return_value = []
        self.b = mock_Backstores(None)

        assert self.b.selected == "rbd"

    @mock.patch('glob.glob')
    def test_detect_existing(self, mock_subproc_glob):
        Common.config = { 
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive" } 
                        ] 
                    } ] 
                } ] }

        mock_subproc_glob.return_value = [ "/s/k/c/t/c/BACKSTORE_0/archive" ]
        self.b = Backstores(None)
        assert self.b.selected == "BACKSTORE"

    def test_rbd(self):

        Common.config = { 
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive" } 
                        ] 
                    } ] 
                } ] }
        class mock_Backstores(Backstores):
              def _load_modules(self):
                  pass

        self.b = mock_Backstores("rbd")
        assert self.b.cmds == [['targetcli', '/backstores/rbd', 'create', 'name=archive', 'dev=/dev/rbd/rbd/archive']]

    @mock.patch('glob.glob')
    def test_rbd_does_nothing(self, mock_subproc_glob):
        Common.config = { 
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive" } 
                        ] 
                    } ] 
                } ] }
        class mock_Backstores(Backstores):
              def _load_modules(self):
                  pass

        mock_subproc_glob.return_value = "globbed/path/name"
        self.b = mock_Backstores("rbd")
        assert not self.b.cmds


    @mock.patch('lrbd.popen')
    def test_create(self, mock_subproc_popen):
        Common.config = { 
            "pools": [ 
                { "pool": "rbd", 
                  "gateways": [
                    { "host": "igw1", "tpg": [ 
                        { "image": "archive" } 
                        ] 
                    } ] 
                } ] }

        self.b = Backstores("iblock")
        self.b.create()
        assert mock_subproc_popen.called

