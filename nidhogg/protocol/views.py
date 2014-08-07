from json import loads

from flask import request
from flask.views import MethodViewType, View

from protocol import exceptions as exc
from common.utils import json_response


class YggdrasilView(View, metaclass=MethodViewType):
    """Class-based view as wrapper for HTTP API"""

    decorators = [json_response]

    def dispatch_request(self, *args, **kwargs):

        try:
            endpoint = args[0]
        except IndexError:
            raise exc.NotFound

        if request.method != "POST":
            raise exc.MethodNotAllowed

        if request.mimetype != "application/json":
            raise exc.BadPayload

        try:
            payload = loads(request.data)
            method = getattr(self, endpoint)
        except ValueError:
            raise exc.BadPayload
        except AttributeError:
            raise exc.NotFound
        else:
            return method(payload)

    @staticmethod
    def authenticate(payload):
        return

    @staticmethod
    def refresh(payload):
        return

    @staticmethod
    def validate(payload):
        return

    @staticmethod
    def signout(payload):
        return

    @staticmethod
    def invalidate(payload):
        return
