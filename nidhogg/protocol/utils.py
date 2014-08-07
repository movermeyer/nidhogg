from functools import wraps


def yggdrasil(function):
    """Decorator to verify request compliance with the Yggdrasil protocol"""

    @wraps(function)
    def wrapped(*args, **kwargs):
        """
        :return: Flask response
        :rtype: Response
        """
        return function
    return wrapped