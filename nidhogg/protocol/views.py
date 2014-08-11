from flask import request
from flask.views import MethodViewType, View

from protocol import exceptions as exc
from protocol import request as req
from common.utils import json_response


class YggdrasilView(View, metaclass=MethodViewType):
    """Class-based view as wrapper for HTTP API"""

    decorators = [json_response]

    def dispatch_request(self, *args, **kwargs):

        try:
            endpoint = kwargs['method']
        except KeyError:
            raise exc.NotFound

        if request.method != "POST":
            raise exc.MethodNotAllowed

        if request.mimetype != "application/json":
            raise exc.BadRequest

        try:
            method = getattr(self, endpoint)
        except AttributeError:
            raise exc.NotFound

        return method(request.data)

    @staticmethod
    def authenticate(raw_data):
        return req.Authenticate(raw_data).result

    @staticmethod
    def refresh(raw_data):
        return req.Refresh(raw_data).result

    @staticmethod
    def validate(raw_data):
        return req.Validate(raw_data).result

    @staticmethod
    def signout(raw_data):
        return req.Signout(raw_data).result

    @staticmethod
    def invalidate(raw_data):
        return req.Invalidate(raw_data).result
