from unittest import TestCase

from nidhogg.common.hashers import generic, wordpress


class TestGenericHasher(TestCase):
    password = '12345'
    hash = '12345'

    def test_check_password(self):
        self.assertTrue(
            generic.check_password(raw=self.password, hashed=self.hash)
        )


class TestWordpressHasher(TestCase):

    password = '1234567890'
    hashes = {
        '$P$9MNSyFf9Kr6gI/e64hs1jwj702dCFH0',
        '$P$9w.70QXPsDPKVh6xYvZjiyPh2GtwyW/',
        '$P$9JKSFWflX4bKzltjjq9M99OXlGD48j1',
        '$P$9uE4OOUl/rb8VaH09EiE1tJTqVheYX1',
        '$P$9MMGuDOAVLG1PNFnqA8OYdTHZ6JBjb/'
    }

    def test_check_password(self):
        for hash in self.hashes:
            self.assertTrue(
                wordpress.check_password(raw=self.password, hashed=hash)
        )