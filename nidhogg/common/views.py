"""Class-based request view for passing HTTP requests to Request instances"""

from flask import request
from flask.views import View

from nidhogg.protocol.yggdrasil import exceptions as exc


class MethodView(View):
    """Class-based view as wrapper for HTTP API"""

    def dispatch_request(self, *args, **kwargs):
        """
        Dispatches request to endpoint or
        return NotFound as JSON'ified error.
        """
        try:
            endpoint = kwargs['method']
        except KeyError:
            raise exc.NotFound

        try:
            method = getattr(self, endpoint)
        except AttributeError:
            raise exc.NotFound

        return method(request.data)
