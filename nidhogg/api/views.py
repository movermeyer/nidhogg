from nidhogg.common.decorators import method
from nidhogg.common.json import json_response
from nidhogg.common.views import MethodView


class ApiView(MethodView):

    @staticmethod
    @method('GET')
    @json_response
    def profile():
        """This will return the uuid of the name at the timestamp provided."""

    @staticmethod
    @method('GET')
    @json_response
    def names():
        """Returns all the usernames this user has used in the past
         and the one they are using currently."""

    @staticmethod
    @method('POST')
    @json_response
    def uuids():
        """This will return the player's username to UIS"""

    @staticmethod
    @method('POST')
    @json_response
    def full():
        """This will return the player's username
        plus any additional information about them (e.g. skins)."""