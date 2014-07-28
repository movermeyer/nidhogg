import unittest
from application import create_app


class TestNidhogg(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        create_app('settings')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()