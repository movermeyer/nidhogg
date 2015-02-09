"""Class-based request view for passing HTTP requests to Request instances"""
from nidhogg.common.json import json_response
from nidhogg.common.views import MethodView
from nidhogg.common.decorators import method, mime
from auth import request as req


class YggdrasilView(MethodView):
    """Class-based view as wrapper for HTTP API"""

    @method("POST")
    @mime("application/json")
    def dispatch_request(self, *args, **kwargs):
        return super().dispatch_request(*args, **kwargs)

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
