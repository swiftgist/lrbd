
from lrbd import main, Configs, Images
import unittest, mock
import re, tempfile
import argparse

class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.args = argparse.Namespace()
        self.args.config = None
        self.args.ceph = "/etc/motd"
        self.args.host = None
        self.args.verbose = False
        self.args.debug = False
        self.args.name = "client.admin"
        self.args.pools = []

    @mock.patch('lrbd.Configs.wipe')
    def test_main_wipe(self, mock_subproc_wipe):
        self.args.wipe = True
        main(self.args)
        assert mock_subproc_wipe.called

    @mock.patch('lrbd.Configs.clear')
    def test_main_clear(self, mock_subproc_clear):
        self.args.wipe = False
        self.args.clear = True
        self.args.unmap = False
        main(self.args)
        assert mock_subproc_clear.called

    @mock.patch('lrbd.Configs.clear')
    @mock.patch('lrbd.Images.__init__')
    @mock.patch('lrbd.Images.unmap')
    def test_main_clear_and_unmap(self, mock_clear, mock_init, mock_unmap):
        self.args.wipe = False
        self.args.clear = True
        self.args.unmap = True
        mock_init.return_value = None
        main(self.args)
        assert (mock_clear.called and mock_unmap.called)

    @mock.patch('lrbd.Images')
    def test_main_unmap(self, mock_Images):
        self.args.wipe = False
        self.args.clear = False
        self.args.unmap = True
        main(self.args)
        assert mock_Images.called

    @mock.patch('lrbd.Configs.wipe')
    @mock.patch('lrbd.Content')
    def test_main_file(self, mock_wipe, mock_Content):
        self.args.wipe = False
        self.args.clear = False
        self.args.unmap = False
        self.args.file = True
        main(self.args)
        assert (mock_wipe.called and mock_Content.called)

    @mock.patch('lrbd.Content')
    def test_main_add(self, mock_Content):
        self.args.wipe = False
        self.args.clear = False
        self.args.unmap = False
        self.args.file = False
        self.args.add = True
        main(self.args)
        assert mock_Content.called

    @mock.patch('lrbd.Configs')
    def test_main_output(self, mock_Configs):
        self.args.wipe = False
        self.args.clear = False
        self.args.unmap = False
        self.args.file = False
        self.args.add = False
        self.args.output = True
        main(self.args)
        assert mock_Configs.called

    @mock.patch('lrbd.Configs')
    @mock.patch('lrbd.Content')
    def test_main_edit(self, mock_Configs, mock_Content):
        self.args.wipe = False
        self.args.clear = False
        self.args.unmap = False
        self.args.file = False
        self.args.add = False
        self.args.output = False
        self.args.edit = True
        self.args.editor = None
        self.args.migrate = False
        main(self.args)
        assert (mock_Configs.called and mock_Content.called)

    @mock.patch('lrbd.Configs')
    def test_main_local(self, mock_Configs):
        self.args.wipe = False
        self.args.clear = False
        self.args.unmap = False
        self.args.file = False
        self.args.add = False
        self.args.output = False
        self.args.edit = False
        self.args.local = True
        self.args.migrate = False
        main(self.args)
        assert mock_Configs.called

    @mock.patch('lrbd.Configs')
    @mock.patch('lrbd.Images')
    @mock.patch('lrbd.Backstores')
    @mock.patch('lrbd.Iscsi')
    @mock.patch('lrbd.TPGs')
    @mock.patch('lrbd.Luns')
    @mock.patch('lrbd.TPGattributes')
    @mock.patch('lrbd.Portals')
    @mock.patch('lrbd.Acls')
    @mock.patch('lrbd.Map')
    @mock.patch('lrbd.Auth')
    def test_main_default(self, mock_Configs, mock_Images, mock_Backstores, mock_Iscsi, mock_TPGs, mock_Luns, mock_Portals, mock_TPGattributes, mock_Acls, mock_Map, mock_Auth):
        self.args.wipe = False
        self.args.clear = False
        self.args.unmap = False
        self.args.file = False
        self.args.add = False
        self.args.output = False
        self.args.edit = False
        self.args.local = False
        self.args.migrate = False
        self.args.backstore = "iblock"
        main(self.args)
        assert (mock_Configs.called and
                mock_Images.called and
                mock_Backstores.called and
                mock_Iscsi.called and
                mock_TPGs.called and
                mock_Luns.called and
                mock_Portals.called and
                mock_TPGattributes.called and
                mock_Acls.called and
                mock_Map.called and
                mock_Auth.called)





