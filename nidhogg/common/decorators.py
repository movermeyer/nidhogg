from functools import wraps

from flask import request

from nidhogg.protocol import exceptions as exc


def method(name):
    """Restrict request method

    :param name: Method name
    :type name: str
    :return: Decorator
    :rtype: callable
    :raise exc.MethodNotAllowed:
    """

    def decorator(function):
        """
        :param function: Function or method to decorate
        :type function: callable
        :return: Decorated function
        :rtype: callable
        :raise exc.MethodNotAllowed:
        """

        @wraps(function)
        def wrapped(*args, **kwargs):
            if request.method != name:
                raise exc.MethodNotAllowed
            return function(*args, **kwargs)

        return wrapped

    return decorator


def mime(mimetype):
    """Restrict request MIME type

    :param mimetype: MIME type name
    :type mimetype: str
    :return: Decorator
    :rtype: callable
    :raise exc.BadRequest:
    """

    def decorator(function):
        """
        :param function: Function or method to decorate
        :type function: callable
        :return: Decorated function
        :rtype: callable
        """

        @wraps(function)
        def wrapped(*args, **kwargs):
            if request.mimetype != mimetype:
                raise exc.BadRequest
            return function(*args, **kwargs)

        return wrapped

    return decorator
