import unittest
from flask import url_for
from tests.base import BaseTestCase


class TestNidhogg(BaseTestCase):

    def test_render(self):
        resp = self.client.get(url_for('pages_app.index'))
        self.assertStatus(resp, 200)
        self.assertIn('Nidhogg Admin', resp.data.decode('utf-8'))

    def test_tokens(self):
        self.fill_db()
        resp = self.client.get(url_for('ajax_app.tokens'))
        self.assertStatus(resp, 200)

if __name__ == '__main__':
    unittest.main()