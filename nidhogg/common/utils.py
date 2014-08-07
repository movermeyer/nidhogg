from functools import wraps
from json import dumps
from flask import make_response


def json_response(function):
    """Decorator for json response from views"""

    @wraps(function)
    def wrapped(*args, **kwargs):
        """Return function result as Flask response with json string payload

        :return: Flask response
        :rtype: Response
        """
        result = function(*args, **kwargs)
        result = dumps(result)
        response = make_response(result)
        response.mimetype = 'application/json'
        return response
    return wrapped
