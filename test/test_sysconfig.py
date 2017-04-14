
from lrbd import sysconfig_options
import unittest
import re, tempfile

class SysconfigTestCase(unittest.TestCase):

    def test_sysconfig_options(self):
        data = '''LRBD_OPTIONS="-v"'''
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tmpfile:
            tmpfile.write(data)
            tmpfile.flush()
            result = sysconfig_options(tmpfile.name)
            print result
            assert result == ['-v']

    def test_sysconfig_options_missing_variable(self):
        data = '''#Just a comment'''
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tmpfile:
            tmpfile.write(data)
            tmpfile.flush()
            result = sysconfig_options(tmpfile.name)
            assert result == []




