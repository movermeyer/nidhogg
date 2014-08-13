import unittest

from nidhogg.common.hashers import generic


class TestGenericHasher(unittest.TestCase):
    password = '12345'
    hash = '12345'

    def test_check_password(self):
        self.assertTrue(
            generic.check_password(raw=self.password, hash=self.hash)
        )

    def test_set_password(self):
        self.assertTrue(
            self.hash,
            generic.set_password(raw=self.password)
        )