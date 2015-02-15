"""Payload data schemas"""

from colander import MappingSchema
from colander import SchemaNode
from colander import String, Integer
from colander import Length, OneOf

from nidhogg.common.utils import generate_token


AGENT = {"name": "Minecraft", "version": 1}
str_validator = Length(min=8, max=255)


class AccessToken(MappingSchema):
    """Access token"""
    accessToken = SchemaNode(String(), validator=str_validator)


class ClientToken(MappingSchema):
    """Client token"""
    clientToken = SchemaNode(String(), validator=str_validator)


class TokensPair(AccessToken, ClientToken):
    """Token pair mapping"""


class Credentials(MappingSchema):
    """Credentials mapping with login and password"""
    username = SchemaNode(String(), validator=str_validator)
    password = SchemaNode(String(), validator=str_validator)


class Profile(MappingSchema):
    """Selected profile mapping"""
    id = SchemaNode(String(), validator=str_validator)
    name = SchemaNode(String(), validator=str_validator)


class Agent(MappingSchema):
    name = SchemaNode(String(), validator=OneOf(["Minecraft"]))
    version = SchemaNode(Integer(), validator=OneOf([1]))


class Refresh(TokensPair):
    """Refresh payload"""
    selectedProfile = Profile()


class Authenticate(Credentials):
    """Auth payload"""
    agent = Agent()
    clientToken = SchemaNode(String(), validator=str_validator, missing=generate_token())
