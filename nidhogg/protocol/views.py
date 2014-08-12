from flask import request
from flask.views import View

from nidhogg.protocol import exceptions as exc
from nidhogg.protocol import request as req
from nidhogg.common.utils import json_response


class YggdrasilView(View):
    """Class-based view as wrapper for HTTP API"""

    methods = ['GET', 'POST']

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
    @json_response
    def authenticate(raw_data):
        instance = req.Authenticate(raw_data)
        instance.process()
        return instance.result

    @staticmethod
    @json_response
    def refresh(raw_data):
        instance = req.Refresh(raw_data)
        instance.process()
        return instance.result

    @staticmethod
    def validate(raw_data):
        instance = req.Validate(raw_data)
        instance.process()
        return ''

    @staticmethod
    def signout(raw_data):
        instance = req.Signout(raw_data)
        instance.process()
        return ''

    @staticmethod
    def invalidate(raw_data):
        instance = req.Invalidate(raw_data)
        instance.process()
        return ''
