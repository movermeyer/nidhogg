import unittest
import uuid

from application import create_app
from common.database import db
from common.models import User, Token


class BaseTestCase(unittest.TestCase):
    def __call__(self, result=None):
        self._pre_setup()
        super(BaseTestCase, self).__call__(result)
        self._post_teardown()

    def _pre_setup(self):
        self.app = create_app('settings_test')
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def _post_teardown(self):
        self.ctx.pop()

    def setUp(self):
        db.create_all(app=self.app)

    def tearDown(self):
        db.drop_all(app=self.app)

    def fill_db(self):
        db.session.add(User(
            login="Twilight",
            email="twilight_sparkle@ponyville.eq",
            password="12345",
            token=Token(value=str(uuid.uuid1()))
        ))
        db.session.add(User(
            login="Luna",
            email="luna@canterlot.eq",
            password="night",
            token=Token(value=str(uuid.uuid1()))
        ))
        db.session.add(User(
            login="CarrotTop",
            email="carrot@ponymail.eq",
            password="first_pie",
            token=Token(value=str(uuid.uuid1()))
        ))
        db.session.commit()

    def assertRedirects(self, resp, location):
        self.assertTrue(resp.status_code in (301, 302))
        self.assertEqual(resp.location, 'http://localhost' + location)

    def assertStatus(self, resp, status_code):
        self.assertEqual(resp.status_code, status_code)