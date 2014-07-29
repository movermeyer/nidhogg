from json import dumps
from flask import make_response


def make_json_response(obj):
    """Make json response from jsonable object

    :param obj: object
    :return: Flask response
    :rtype: Response
    """
    value = dumps(obj)
    response = make_response(value)
    response.mimetype = 'application/json'
    return response