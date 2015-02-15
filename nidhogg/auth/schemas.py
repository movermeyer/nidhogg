"""Payload data schemas"""

from colander import MappingSchema
from colander import SchemaNode
from colander import String, Integer
from colander import Length, OneOf

from nidhogg.common.utils import generate_token


AGENT = {"name": "Minecraft", "version": 1}


class AccessToken(MappingSchema):
    """Access token"""
    accessToken = SchemaNode(String(), validator=Length(min=8, max=255))


class ClientToken(MappingSchema):
    """Client token"""
    clientToken = SchemaNode(String(), validator=Length(min=8, max=255))


class TokensPair(AccessToken, ClientToken):
    """Token pair mapping"""


class Credentials(MappingSchema):
    """Credentials mapping with login and password"""
    username = SchemaNode(String(), validator=Length(min=8, max=255))
    password = SchemaNode(String(), validator=Length(min=8, max=255))


class Profile(MappingSchema):
    """Selected profile mapping"""
    id = SchemaNode(String(), validator=Length(min=8, max=255))
    name = SchemaNode(String(), validator=Length(min=8, max=255))


class Agent(MappingSchema):
    name = SchemaNode(String(), validator=OneOf(["Minecraft"]))
    version = SchemaNode(Integer(), validator=OneOf([1]))


class Refresh(TokensPair):
    """Refresh payload"""
    selectedProfile = Profile()


class Authenticate(Agent, Credentials):
    """Auth payload"""
    agent = Agent()
    clientToken = SchemaNode(String(), validator=Length(min=8, max=255), missing=generate_token())
