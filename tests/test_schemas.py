from itertools import product
from random import choice
from string import ascii_letters
from unittest import TestCase

from colander import Invalid

from nidhogg.auth import schemas


class YggdrasilSchemasTest(TestCase):

    @staticmethod
    def generate_str(length):
        return ''.join([choice(ascii_letters) for _ in range(length)])

    @classmethod
    def setUpClass(cls):
        cls.valid_str = cls.generate_str(10)

        cls.not_valid = (
            cls.generate_str(5),
            cls.generate_str(500),
            123456,
            123.456,
            False,
            True,
            None,
            (),
        )

    def tearDown(self):
        self.schema = None


class AccessTokenTest(YggdrasilSchemasTest):

    def setUp(self):
        self.schema = schemas.AccessToken()

    def test_valid_token(self):
        payload = {"accessToken": self.valid_str}
        self.assertEqual(self.schema.deserialize(payload), payload)

    def test_invalid_payload(self):
        for payload in self.not_valid:
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_values(self):
        for payload in (
            dict([pair])
            for pair
            in product(["accessToken"], self.not_valid)
        ):
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_keys(self):
        for payload in (
            dict([pair])
            for pair
            in product(self.not_valid, self.not_valid)
        ):
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)


class ClientTokenTest(YggdrasilSchemasTest):

    def setUp(self):
        self.schema = schemas.ClientToken()

    def test_valid_token(self):
        payload = {"clientToken": self.valid_str}
        self.assertEqual(self.schema.deserialize(payload), payload)

    def test_invalid_payload(self):
        for payload in self.not_valid:
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_values(self):
        for payload in (
            dict([pair])
            for pair
            in product(["clientToken"], self.not_valid)
        ):
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_keys(self):
        for payload in (
            dict([pair])
            for pair
            in product(self.not_valid, self.not_valid)
        ):
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)


class TokensPairTest(YggdrasilSchemasTest):

    def setUp(self):
        self.schema = schemas.TokensPair()

    def test_valid_tokens(self):
        payload = {"accessToken": self.valid_str, "clientToken": self.valid_str}
        self.assertEqual(self.schema.deserialize(payload), payload)

    def test_invalid_payload(self):
        for payload in self.not_valid:
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_values(self):
        for payload in (
            dict(pair)
            for pair
            in product(
                product(["accessToken"], self.not_valid),
                product(["clientToken"], self.not_valid),
            )
        ):
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_keys(self):
        for payload in (
            dict(pair)
            for pair
            in product(
                product(self.not_valid, self.not_valid),
                product(self.not_valid, self.not_valid)
            )
        ):
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)


class CredentialsTest(YggdrasilSchemasTest):

    def setUp(self):
        self.schema = schemas.Credentials()

    def test_valid_credentials(self):
        payload = {"username": self.valid_str, "password": self.valid_str}
        self.assertEqual(self.schema.deserialize(payload), payload)

    def test_invalid_payload(self):
        for payload in self.not_valid:
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_values(self):
        for payload in (
            dict(pair)
            for pair
            in product(
                product(["username"], self.not_valid),
                product(["password"], self.not_valid),
            )
        ):
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_keys(self):
        for payload in (
            dict(pair)
            for pair
            in product(
                product(self.not_valid, self.not_valid),
                product(self.not_valid, self.not_valid)
            )
        ):
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)


class ProfileTest(YggdrasilSchemasTest):

    def setUp(self):
        self.schema = schemas.Profile()

    def test_valid_profile(self):
        payload = {"id": self.valid_str, "name": self.valid_str}
        self.assertEqual(self.schema.deserialize(payload), payload)

    def test_invalid_payload(self):
        for payload in self.not_valid:
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_values(self):
        for payload in (
            dict(pair)
            for pair
            in product(
                product(["id"], self.not_valid),
                product(["name"], self.not_valid),
            )
        ):
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_keys(self):
        for payload in (
            dict(pair)
            for pair
            in product(
                product(self.not_valid, self.not_valid),
                product(self.not_valid, self.not_valid)
            )
        ):
            with self.assertRaises(Invalid):
                self.schema.deserialize(payload)


class AgentTest(YggdrasilSchemasTest):

    def setUp(self):
        self.schema = schemas.Agent()

    def test_valid_agent(self):
        self.assertEqual(self.schema.deserialize(schemas.AGENT), schemas.AGENT)

    def test_invalid_agent_name(self):
        payload = {"name": "test", "version": 1}
        with self.assertRaises(Invalid):
                self.schema.deserialize(payload)

    def test_invalid_agent_version(self):
        payload = {"name": "Minecraft", "version": 2}
        with self.assertRaises(Invalid):
                self.schema.deserialize(payload)


class RefreshTest(YggdrasilSchemasTest):

    def setUp(self):
        self.schema = schemas.Refresh()

    def test_valid_refresh(self):
        payload = {
            "accessToken": self.valid_str,
            "clientToken": self.valid_str,
            "selectedProfile": {
                "id": self.valid_str,
                "name": self.valid_str
            }
        }
        self.assertEqual(self.schema.deserialize(payload), payload)


class AuthenticateTest(YggdrasilSchemasTest):

    def setUp(self):
        self.schema = schemas.Authenticate()
        self.payload = {
            "username": self.valid_str,
            "password": self.valid_str,
            "agent": schemas.AGENT,
        }

    def test_valid_authenticate_with_token(self):
        self.payload["clientToken"] = self.valid_str
        self.assertEqual(self.schema.deserialize(self.payload), self.payload)

    def test_valid_authenticate_without_token(self):
        result = self.schema.deserialize(self.payload)
        self.assertIn("clientToken", result)
        client_token = result["clientToken"]
        self.assertIsInstance(client_token, str)
        self.assertIsNotNone(client_token)
