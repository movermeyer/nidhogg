from itertools import product
import json

from common.models import User, Token

from protocol import request as req
from protocol import exceptions as exc
from tests.base import BaseTestCase


class RequestTest(BaseTestCase):
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
        request.process()
        result = request.result
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
        request.process()
        result = request.result

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
        request.process()
        result = request.result

        self.assertIn("clientToken", result)
        self.assertEqual(payload["clientToken"], result["clientToken"])


class RefreshTest(BaseTestCase):
    def test_invalid_payload(self):
        values = (123, True, [1], {2: 3}, "")
        access_tokens = product(["accessToken"], values)
        client_tokens = product(["clientToken"], values)
        pairs = list(product(list(access_tokens), list(client_tokens)))
        probes = [dict(pair) for pair in pairs]

        for pair in probes:
            with self.assertRaises(exc.InvalidToken):
                req.Refresh(json.dumps(pair))

    def test_invalid_token(self):
        payload = {"clientToken": "nonexistent token"}

        with self.assertRaises(exc.InvalidToken):
            request = req.Refresh(json.dumps(payload))
            request.process()

    def test_success_refresh(self):
        payload = {
            "username": "twilight_sparkle@ponyville.eq",
            "password": "12345",
        }
        request = req.Authenticate(json.dumps(payload))
        request.process()
        result = request.result
        token = Token.query.filter(Token.client == result["clientToken"]).one()
        old_token_values = (token.access, token.client)

        refresh_request = req.Refresh(json.dumps(result))
        refresh_request.process()
        refresh_result = refresh_request.result
        fresh_token = (
            Token.query
            .filter(Token.client == refresh_result["clientToken"])
            .one()
        )
        new_token_values = (token.access, token.client)

        self.assertNotEqual(result, fresh_token)
        self.assertNotEqual(old_token_values, new_token_values)

        self.assertEqual(refresh_result["accessToken"], token.access)
        self.assertEqual(refresh_result["clientToken"], token.client)


class ValidateTest(BaseTestCase):
    def test_invalid_payload(self):
        payloads = ({}, {"accessToken": 123}, {"accessToken": ""})

        for payload in payloads:
            with self.assertRaises(exc.BadPayload):
                req.Validate(json.dumps(payload))

    def test_invalid_token(self):
        payload = {"accessToken": "nonexistent token"}

        with self.assertRaises(exc.InvalidToken):
            request = req.Validate(json.dumps(payload))
            request.process()

    def test_successful_validate(self):
        payload = {
            "username": "twilight_sparkle@ponyville.eq",
            "password": "12345"
        }
        request = req.Authenticate(json.dumps(payload))
        request.process()

        payload = {"accessToken": request.result["accessToken"]}
        request = req.Validate(json.dumps(payload))
        request.process()


class SignoutTest(BaseTestCase):
    def test_successful_signout(self):
        payload = {
            "username": "twilight_sparkle@ponyville.eq",
            "password": "12345"
        }
        user = User.query.filter(User.email == payload["username"]).one()
        token_id = user.token.id
        request = req.Signout(json.dumps(payload))
        request.process()

        self.assertIsNone(user.token)
        self.assertIsNone(Token.query.get(token_id))


class InvalidateTest(BaseTestCase):
    def test_successful_invalidate(self):
        payload = {
            "username": "twilight_sparkle@ponyville.eq",
            "password": "12345"
        }
        user = User.query.filter(User.email == payload["username"]).one()
        token_id = user.token.id

        request = req.Authenticate(json.dumps(payload))
        request.process()
        result = request.result

        invalidate_request = req.Invalidate(json.dumps(result))
        invalidate_request.process()

        self.assertIsNone(user.token)
        self.assertIsNone(Token.query.get(token_id))
