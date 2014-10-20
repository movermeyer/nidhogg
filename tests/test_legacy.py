from nidhogg.common.models import User
from nidhogg.common.utils import generate_token
from nidhogg.protocol.legacy import request as req
from nidhogg.protocol.legacy import exceptions as exc

from tests import BaseTestCase


class LegacyRequestTest(BaseTestCase):
    def test_wrong_argument(self):
        with self.assertRaises(exc.BadPayload):
            req.LegacyRequest([])
        with self.assertRaises(exc.BadPayload):
            req.LegacyRequest(b'123')

    def test_unimplemented_process(self):
        with self.assertRaises(NotImplementedError):
            req.LegacyRequest({"first_key": "first_value"}).process()

    def test_wrong_key_value_types(self):
        with self.assertRaises(exc.BadPayload):
            req.LegacyRequest({1: "2"})
        with self.assertRaises(exc.BadPayload):
            req.LegacyRequest({"3": 4})

    def test_empty_payload(self):
        with self.assertRaises(exc.EmptyPayload):
            req.LegacyRequest({})

    def test_save_payload(self):
        payload = {"first_key": "first_value", "second_arg": "second_value"}
        r = req.LegacyRequest(payload)
        self.assertEqual(payload, r.payload)

    def test_token_method(self):
        token = generate_token()
        self.assertIsInstance(token, str)
        self.assertEqual(len(token), 32)
        self.assertIsInstance(int(token, 16), int)

    def test_result_tuple(self):
        payload = {"first_key": "first_value", "second_arg": "second_value"}
        r = req.LegacyRequest(payload)
        result = ('first', "second")
        r._result = result
        self.assertEqual(r.result, "first:second")

    def test_result_str(self):
        payload = {"first_key": "first_value", "second_arg": "second_value"}
        r = req.LegacyRequest(payload)
        result = "OK"
        r._result = result
        self.assertEqual(r.result, "OK")


class AuthenticateTest(BaseTestCase):
    def test_empty_credentials(self):
        with self.assertRaises(exc.EmptyCredentials):
            payload = {"key": "strange"}
            req.Authenticate(payload)

        with self.assertRaises(exc.EmptyCredentials):
            payload = {"user": "Twilight"}
            req.Authenticate(payload)

        with self.assertRaises(exc.EmptyCredentials):
            payload = {"password": "12345"}
            req.Authenticate(payload)

    def test_no_such_user(self):
        payload = {
            "user": "pinkie_pie@ponyville.eq",
            "password": "12345",
        }
        with self.assertRaises(exc.InvalidCredentials):
            request = req.Authenticate(payload)
            request.process()

    def test_wrong_password(self):
        payload = {
            "user": "twilight_sparkle@ponyville.eq",
            "password": "123456",
        }
        with self.assertRaises(exc.InvalidCredentials):
            request = req.Authenticate(payload)
            request.process()

    def test_success_simple(self):
        payload = {
            "user": "twilight_sparkle@ponyville.eq",
            "password": "12345",
        }
        request = req.Authenticate(payload)
        request.process()
        result = request.result.split(":")
        user = User.query.filter(User.email == payload["user"]).one()

        self.assertEqual(result[3], user.token.access)
        self.assertEqual(result[4], user.token.client)


class ValidateTest(BaseTestCase):
    def test_invalid_payload(self):
        with self.assertRaises(exc.EmptyCredentials):
            payload = {"key": "strange"}
            req.Authenticate(payload)

        with self.assertRaises(exc.EmptyCredentials):
            payload = {"user": "Twilight"}
            req.Authenticate(payload)

        with self.assertRaises(exc.EmptyCredentials):
            payload = {"sessionId": "12345"}
            req.Authenticate(payload)

    def test_invalid_token(self):
        payload = {
            "user": "twilight_sparkle@ponyville.eq",
            "sessionId": "nothing"
        }

        with self.assertRaises(exc.BadPayload):
            request = req._Validate(payload)
            request.process()

    def test_successful_validate(self):
        payload = {
            "user": "twilight_sparkle@ponyville.eq",
            "password": "12345"
        }
        request = req.Authenticate(payload)
        request.process()

        payload = {
            "user": payload["user"],
            "sessionId": request.result.split(":")[3]
        }
        request = req._Validate(payload)
        request.process()


class CheckTest(BaseTestCase):
    def test_ok_check(self):
        payload = {
            "user": "twilight_sparkle@ponyville.eq",
            "password": "12345"
        }
        request = req.Authenticate(payload)
        request.process()

        payload = {
            "user": payload["user"],
            "sessionId": request.result.split(":")[3]
        }
        request = req.Check(payload)
        request.process()

        self.assertEqual(request.result, "YES")


class JoinTest(BaseTestCase):
    def test_ok_check(self):
        payload = {
            "user": "twilight_sparkle@ponyville.eq",
            "password": "12345"
        }
        request = req.Authenticate(payload)
        request.process()

        payload = {
            "user": payload["user"],
            "sessionId": request.result.split(":")[3]
        }
        request = req.Join(payload)
        request.process()

        self.assertEqual(request.result, "OK")
