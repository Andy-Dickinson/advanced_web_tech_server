# test file for testing.py
# to use, run in terminal with python
# should run tests after each edit of code

import unittest
import testing # flask app imported so accessible from this test script


# write all tests in here
class TestHarness(unittest.TestCase):
    def test_root(self):
        self.app = testing.app.test_client()
        out = self.app.get('/')

        # tests status in response
        assert '200 OK' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type


    # test fails if uncomment 200 code check
    def test_error_case(self):
        self.app = testing.app.test_client()
        out = self.app.get('/a_nonExistent_page')

        # assert '200 OK' in out.status
        assert '404' in out.status


if __name__== '__main__':
    unittest.main()