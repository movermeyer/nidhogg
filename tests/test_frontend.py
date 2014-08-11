import json

from flask import url_for

from common.models import User
from common.utils import json_datetime_hook
from tests.base import BaseTestCase


class MainTest(BaseTestCase):
    def test_render(self):
        resp = self.client.get(url_for('pages_app.index'))
        self.assertStatus(resp, 200)
        self.assertIn('Nidhogg Admin', resp.data.decode('utf-8'))

    def test_tokens(self):
        self.fill_db()
        resp = self.client.get(url_for('ajax_app.tokens'))
        self.assertStatus(resp, 200)

    def test_single_token(self):
        self.fill_db()
        resp = self.client.get(url_for('ajax_app.tokens')).data.decode('utf-8')
        data = json.loads(resp, object_hook=json_datetime_hook)
        db_user = User.query.filter(User.login == "Twilight").first()
        data_user = next(filter(lambda x: x['login'] == "Twilight", data))
        self.assertEqual(db_user.email, data_user['email'])
        self.assertEqual(db_user.login, data_user['login'])
        self.assertEqual(db_user.id, data_user['id'])
        self.assertEqual(db_user.token.created, data_user['created'])
