import json

from flask import url_for

from nidhogg.common.models import User
from nidhogg.common.utils import json_datetime_hook
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


class ApiTest(BaseTestCase):
    def send_payload(self, url, payload):
        return self.client.post(
            path=url,
            content_type='application/json',
            data=json.dumps(payload)
        )

    def make_auth(self):
        payload = {
            "username": "twilight_sparkle@ponyville.eq",
            "password": "12345",
        }
        return self.send_payload(
            url_for('generic', method='authenticate'),
            payload
        )

    def test_authenticate(self):
        response = self.make_auth()
        self.assertStatus(response, 200)

    def test_refresh(self):
        result = self.make_auth()
        response = self.send_payload(
            url_for('generic', method='refresh'),
            json.loads(result.data.decode())
        )
        self.assertStatus(response, 200)

    def test_validate(self):
        result = self.make_auth()
        response = self.send_payload(
            url_for('generic', method='validate'),
            {"accessToken": json.loads(result.data.decode())["accessToken"]}
        )
        self.assertStatus(response, 200)
        self.assertEqual(response.data, b'')

    def test_signout(self):
        self.make_auth()
        response = self.send_payload(
            url_for('generic', method='signout'),
            {"username": "twilight_sparkle@ponyville.eq", "password": "12345"}
        )
        self.assertStatus(response, 200)
        self.assertEqual(response.data, b'')

    def test_invalidate(self):
        result = self.make_auth()
        response = self.send_payload(
            url_for('generic', method='invalidate'),
            json.loads(result.data.decode())
        )
        self.assertStatus(response, 200)
        self.assertEqual(response.data, b'')
