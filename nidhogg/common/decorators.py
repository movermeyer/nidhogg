from functools import wraps

from auth import exceptions as exc


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
