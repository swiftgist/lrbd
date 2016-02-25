from lrbd import strip_comments, lstrip_spaces, check_keys, compare_settings, iqn, uniq, Common
from nose.tools import  *
import unittest

class HelpersTestCase(unittest.TestCase):

    def setUp(self):
        Common.config = {}

    def tearDown(self):
        Common.config = {}

    def test_strip_comments(self):
        assert strip_comments("# some comment\n") == ""
    
    def test_strip_comments_unchanged(self):
        assert strip_comments("some code\n") == "some code\n"
    
    def test_lstrip_spaces(self):
        assert lstrip_spaces(" " * 12) == ""
    
    def test_check_keys(self):
        keys = [ "a", "b", "c" ]
        data = { "a": "", "b": "", "c": "" }
        assert check_keys(keys, data, "test_check_keys") == None

    @raises(ValueError)
    def test_check_keys_exception(self):
        keys = [ "a", "b", "c", "d" ]
        data = { "a": "", "b": "", "c": "" }
        check_keys(keys, data, "test_check_keys")

    def test_compare_settings(self):
        keys = [ "a", "b" ]
        current = { "a": "apple", "b": "banana" }
        config = { "a": "apple", "b": "banana", "c": "cherry" }
        assert compare_settings(keys, current, config)

    def test_compare_settings_fails(self):
        keys = [ "a", "b" ]
        current = { "a": "apple", "b": "banana" }
        config = { "a": "apple", "b": "blueberry", "c": "cherry" }
        assert compare_settings(keys, current, config) == False

    def test_iqn(self):
        entry = { 'target': "def" }
        Common.config = { 'iqns' : [ "abc" ] }
        assert iqn(entry) == "def"

    def test_iqn_missing_target(self):
        entry = {}
        Common.config['iqns'] = [ "abc" ] 
        #Common.config = { 'iqns' : [ "abc" ] }
        assert iqn(entry) == "abc"

    # skip test_addresses

    def test_uniq(self):
        a = [ [ "cmd1", "arg1" ],  [ "cmd1", "arg1" ] ]
        b = [ [ "cmd1", "arg1" ] ]
        print uniq(a)
        assert uniq(a) == b

    def test_uniq_sorts(self):
        a = [ [ "cmd2", "arg1" ],  [ "cmd1", "arg1" ] ]
        b = [ [ "cmd1", "arg1" ],  [ "cmd2", "arg1" ] ]
        assert uniq(a) == b

