from functools import wraps
from flask import request
from protocol import exceptions as exc
from json import loads


def yggdrasil(function):
    """Decorator to verify request compliance with the Yggdrasil protocol"""

    @wraps(function)
    def wrapped(*args, **kwargs):
        """
        :return: Flask response
        :rtype: Response
        """
        if request.method != "POST":
            raise exc.MethodNotAllowed

        if request.mimetype != "application/json":
            raise exc.BadPayload

        try:
            payload = loads(request.data)
        except ValueError:
            raise exc.BadPayload
        else:
            return function(payload, *args, **kwargs)

    return wrapped