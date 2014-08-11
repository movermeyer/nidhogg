from itertools import product
import json
from common.models import User

from protocol import request as req
from protocol import exceptions as exc
from tests.base import BaseTestCase


class RequestTestBreak(BaseTestCase):
    def test_wrong_argument(self):
        with self.assertRaises(exc.BadPayload):
            req.Request('[]')
        with self.assertRaises(exc.BadPayload):
            req.Request(b'123')

    def test_unimplemented_process(self):
        with self.assertRaises(NotImplementedError):
            req.Request('{}').process()

    def test_save_payload(self):
        payload = {"1": 2, "3": [1, 2, 3, 4]}
        r = req.Request(json.dumps(payload))
        self.assertEqual(payload, r.payload)

    def test_token_method(self):
        token = req.Request._generate_token()
        self.assertIsInstance(token, str)
        self.assertEqual(len(token), 32)
        self.assertIsInstance(int(token, 16), int)


class AuthenticateTest(BaseTestCase):
    def test_empty_credentials(self):
        with self.assertRaises(exc.EmptyCredentials):
            payload = json.dumps({})
            req.Authenticate(payload)

        with self.assertRaises(exc.EmptyCredentials):
            payload = json.dumps({"username": "Twilight"})
            req.Authenticate(payload)

        with self.assertRaises(exc.EmptyCredentials):
            payload = json.dumps({"password": "12345"})
            req.Authenticate(payload)

    def test_nonstring_credentials(self):
        values = (123, True, [1], {2: 3})
        users = product(["username"], values)
        passwords = product(["password"], values)
        pairs = list(product(list(users), list(passwords)))
        probes = [dict(pair) for pair in pairs]

        for pair in probes:
            with self.assertRaises(exc.InvalidCredentials):
                req.Authenticate(json.dumps(pair))

    def test_agent(self):
        payload = {
            "username": "Twilight",
            "password": "12345",
            "agent": {"name": "Minecraft", "version": 1}
        }
        req.Authenticate(json.dumps(payload))

        payload["agent"]["name"] = 123
        with self.assertRaises(exc.BadPayload):
            req.Authenticate(json.dumps(payload))

    def test_client_token(self):
        payload = {
            "username": "Twilight",
            "password": "12345",
            "clientToken": req.Request._generate_token()
        }
        req.Authenticate(json.dumps(payload))

        payload["clientToken"] = ""
        with self.assertRaises(exc.BadPayload):
            req.Authenticate(json.dumps(payload))

        payload["clientToken"] = {12: 34}
        with self.assertRaises(exc.BadPayload):
            req.Authenticate(json.dumps(payload))

    def test_no_such_user(self):
        payload = {
            "username": "pinkie_pie@ponyville.eq",
            "password": "12345",
        }
        with self.assertRaises(exc.InvalidCredentials):
            request = req.Authenticate(json.dumps(payload))
            request.process()

    def test_wrong_password(self):
        payload = {
            "username": "twilight_sparkle@ponyville.eq",
            "password": "123456",
        }
        with self.assertRaises(exc.InvalidCredentials):
            request = req.Authenticate(json.dumps(payload))
            request.process()

    def test_migration_done(self):
        payload = {
            "username": "Twilight",
            "password": "12345",
        }
        with self.assertRaises(exc.MigrationDone):
            request = req.Authenticate(json.dumps(payload))
            request.process()

    def test_success_simple(self):
        payload = {
            "username": "twilight_sparkle@ponyville.eq",
            "password": "12345",
        }
        request = req.Authenticate(json.dumps(payload))
        result = request.process()
        user = User.query.filter(User.email == payload["username"]).one()

        self.assertIn("accessToken", result)
        self.assertIn("clientToken", result)
        self.assertEqual(result["accessToken"], user.token.access)
        self.assertEqual(result["clientToken"], user.token.client)

    def test_success_agent_profiles(self):
        payload = {
            "username": "twilight_sparkle@ponyville.eq",
            "password": "12345",
            "agent": {"name": "Minecraft", "version": 1}
        }
        request = req.Authenticate(json.dumps(payload))
        result = request.process()
        user = User.query.filter(User.email == payload["username"]).one()
        profile = {"id": user.token.client, "name": user.login}

        self.assertIn("selectedProfile", result)
        self.assertEqual(result["selectedProfile"], profile)

        self.assertIn("availableProfiles", result)
        self.assertEqual(result["availableProfiles"], [profile])

    def test_success_custom_client_token(self):
        payload = {
            "username": "twilight_sparkle@ponyville.eq",
            "password": "12345",
            "clientToken": req.Request._generate_token()
        }
        request = req.Authenticate(json.dumps(payload))
        result = request.process()

        self.assertIn("clientToken", result)
        self.assertEqual(payload["clientToken"], result["clientToken"])
