"""Class-based request view for passing HTTP requests to Request instances"""

from flask import request
from flask.views import View

from nidhogg.legacy import exceptions as exc
from nidhogg.legacy import request as req


class LegacyView(View):
    """Class-based view for legacy auth"""
    methods = ['GET', 'POST']

    def dispatch_request(self, *args, **kwargs):
        try:
            endpoint = kwargs['method']
        except KeyError:
            raise exc.NoSuchMethod

        try:
            method = getattr(self, endpoint)
        except AttributeError:
            raise exc.NoSuchMethod

        return method(request.GET or request.POST)

    @staticmethod
    def authenticate(raw_data):
        instance = req.Authenticate(raw_data)
        instance.process()
        return instance.result

    @staticmethod
    def join(raw_data):
        instance = req.Join(raw_data)
        instance.process()
        return instance.result

    @staticmethod
    def check(raw_data):
        instance = req.Check(raw_data)
        instance.process()
        return instance.result