"""Class-based request view for passing HTTP requests to Request instances"""

from flask import request
from flask.views import View

from nidhogg.protocol import exceptions as exc
from nidhogg.protocol import request as req
from nidhogg.common.utils import json_response


class YggdrasilView(View):
    """Class-based view as wrapper for HTTP API"""

    methods = ['GET', 'POST']

    def dispatch_request(self, *args, **kwargs):
        """
        Dispatches request to endpoint or
        return NotFound as JSON'ified error.
        """
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
        """Authenticate endpoint

        .. note::
            URL: /authenticate

        :type raw_data: bytes
        :rtype: str
        :return: JSON-encoded dict
        """

        instance = req.Authenticate(raw_data)
        instance.process()
        return instance.result

    @staticmethod
    @json_response
    def refresh(raw_data):
        """Refresh endpoint

        .. note::
            URL: /refresh

        :type raw_data: bytes
        :rtype: str
        :return: JSON-encoded dict
        """

        instance = req.Refresh(raw_data)
        instance.process()
        return instance.result

    @staticmethod
    def validate(raw_data):
        """Validate endpoint

        .. note::
            URL: /validate

        :type raw_data: bytes
        :rtype: str
        :return: Empty string (nothing)
        """

        instance = req.Validate(raw_data)
        instance.process()
        return ''

    @staticmethod
    def signout(raw_data):
        """Signout endpoint

        .. note::
            URL: /signout

        :type raw_data: bytes
        :rtype: str
        :return: Empty string (nothing)
        """

        instance = req.Signout(raw_data)
        instance.process()
        return ''

    @staticmethod
    def invalidate(raw_data):
        """Invalidate endpoint

        .. note::
            URL: /invalidate

        :type raw_data: bytes
        :rtype: str
        :return: Empty string (nothing)
        """

        instance = req.Invalidate(raw_data)
        instance.process()
        return ''
