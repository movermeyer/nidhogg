import unittest

from nidhogg.application import create_app
from nidhogg.common.database import db
from nidhogg.common.models import User, Token


class BaseTestCase(unittest.TestCase):
    def __call__(self, result=None):
        self._pre_setup()
        super(BaseTestCase, self).__call__(result)
        self._post_teardown()

    def _pre_setup(self):
        self.app = create_app('settings.main')
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def _post_teardown(self):
        self.ctx.pop()

    def setUp(self):
        db.create_all(app=self.app)
        self.fill_db()

    def tearDown(self):
        db.drop_all(app=self.app)

    def fill_db(self):
        db.session.add(User(
            login="Twilight",
            email="twilight_sparkle@ponyville.eq",
            password="12345",
            token=Token()
        ))
        db.session.add(User(
            login="Luna",
            email="luna@canterlot.eq",
            password="night",
            token=Token()
        ))
        db.session.add(User(
            login="CarrotTop",
            email="carrot@ponymail.eq",
            password="first_pie",
            token=Token()
        ))
        db.session.commit()

    def clear_all_tokens(self):
        db.session.query(Token).delete()
        db.session.commit()

    def assertStatus(self, resp, status_code):
        self.assertEqual(resp.status_code, status_code)
