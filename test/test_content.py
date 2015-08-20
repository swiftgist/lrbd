
from lrbd import *
from nose.tools import  *
import unittest
import re, tempfile

class ContentTestCase(unittest.TestCase):

    def setUp(self):
        self.content = Content()

    def test_instructions(self):
        assert re.match(r'#.*\n', self.content.instructions())

    def test_read(self):
        data = '''{ "pools": [ { "pool": "rbd", 
                             "gateways": [ {
                                 "host": "igw1", 
                                 "tpg": [ {
                                     "image": "archive",
                                     "initiator": "iqn"
                                 } ]
                             } ] 
                         } ] 
                   }'''
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tmpfile:
            tmpfile.write(data)
            tmpfile.flush()
            self.content.read(tmpfile.name)
            assert self.content.submitted

    @raises(IOError)
    def test_read_ioerror(self):
        self.content.read("missing_file")

    @raises(RuntimeError)
    def test_read_runtimeerror(self):
        # Double comma
        data = '''{ "auth": [ { "host": "" } ], ,
                "pools": [ { "gateways": [ { "host": [], "tpg": [] } ] } ] }'''
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tmpfile:
            tmpfile.write(data)
            tmpfile.flush()
            self.content.read(tmpfile.name)

    # test_validate works in test_read

    def test_validate_exception(self):        
        assert self.content.validate("{,}") == False

    def test_verify_mandatory_keys_pools(self):
        try:
            self.content.verify_mandatory_keys("{}")
        except ValueError, e:
            assert re.match(r"Mandatory key 'pools' is missing", str(e))

    def test_verify_mandatory_keys_pool_contents(self):
        try:
            self.content.verify_mandatory_keys('{ "pools": [] }')
        except ValueError, e:
            assert re.match(r"pools have no entries", str(e))

    def test_verify_mandatory_keys_gateways(self):
        data = '{ "pools": [ { "pool": "" } ] }'
        try:
            self.content.verify_mandatory_keys(data) 
        except ValueError, e:
            assert re.match(r"Mandatory key 'gateways' is missing", str(e))

    def test_verify_mandatory_keys_gateways_entries(self):
        data = '{ "pools": [ { "gateways": [] } ] }'
        try:
            self.content.verify_mandatory_keys(data)
        except ValueError, e:
            assert re.match(r"gateways have no entries", str(e))
            

    def test_verify_mandatory_keys_host_or_target(self):
        data = '{ "pools": [ { "gateways": [ { "tpg": [] } ] } ] }'
        try:
            self.content.verify_mandatory_keys(data) 
        except ValueError, e:
            assert re.match(r"Mandatory key 'host' or 'target' is missing", str(e))

    def test_verify_mandatory_keys_tpg(self):
        data = '{ "pools": [ { "gateways": [ { "host": [] } ] } ] }'
        try:
            self.content.verify_mandatory_keys(data) 
        except ValueError, e:
            assert re.match(r"Mandatory key 'tpg' is missing", str(e))

    def test_verify_mandatory_keys_auth(self):
        data = '''{ "auth": [ { "discovery": "" } ], 
                "pools": [ { "gateways": [ { "host": [], "tpg": [] } ] } ] }'''
        try:
            self.content.verify_mandatory_keys(data) 
        except ValueError, e:
            assert re.match(r"Mandatory key 'host' or 'target' is missing from auth", str(e))
            

    # Need to understand mock to do save



    


