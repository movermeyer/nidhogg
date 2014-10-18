from functools import wraps
from json import dumps
from datetime import datetime, date, time, timedelta, tzinfo
import uuid

from flask import make_response
from flask import request
from nidhogg.protocol import exceptions as exc


def generate_token():
    """Generate random UUID token like Java's UUID.toString()

    :rtype: str
    """
    return uuid.uuid1().hex


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

def json_response(function):
    """Decorator for json response from views"""

    @wraps(function)
    def wrapped(*args, **kwargs):
        """Return function result as Flask response with json string payload

        :return: Flask response
        :rtype: Response
        """
        result = function(*args, **kwargs)
        result = dumps(result, default=json_datetime_default)
        response = make_response(result)
        response.mimetype = 'application/json'
        return response

    return wrapped


@json_response
def error_handler(exception):
    """Helper function for proper exception handling in Flask"""
    return exception.data


class Classproperty(property):
    """Property decorator for classes."""

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset):
        self.__offset = timedelta(seconds=offset)

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return 'TZ offset: {secs} hours'.format(secs=self.__offset)

    def dst(self, dt):
        return timedelta(0)


def json_datetime_default(o):
    """Encoder for date/time/datetime objects.
    Usage: json.dumps(object, default=json_datetime_default)

    :type o: datetime | date | time
    :rtype: dict
    :raises: TypeError
    """

    if type(o) == date:
        return {'__date__': [o.year, o.month, o.day]}

    if isinstance(o, time):
        res = {'__time__': [o.hour, o.minute, o.second, o.microsecond]}
        if o.tzinfo is not None:
            res['__tzshift__'] = o.utcoffset().seconds
        return res

    if isinstance(o, datetime):
        res = {'__datetime__': [
            o.year, o.month, o.day, o.hour, o.minute, o.second, o.microsecond
        ]}
        if o.tzinfo is not None:
            res['__tzshift__'] = o.utcoffset().seconds
        return res

    raise TypeError


def json_datetime_hook(dictionary):
    """JSON object_hook function for decoding date/time/datetime objects.
    Usage: json.loads(object, object_hook=json_datetime_hook)

    :type dictionary: dict
    :rtype: datetime | date | time
    """

    if '__date__' in dictionary:
        return date(*dictionary['__date__'])

    if '__time__' in dictionary:
        res = time(*dictionary['__time__'])
        if '__tzshift__' in dictionary:
            res = res.replace(tzinfo=FixedOffset(dictionary['__tzshift__']))
        return res

    if '__datetime__' in dictionary:
        res = datetime(*dictionary['__datetime__'])
        if '__tzshift__' in dictionary:
            res = res.replace(tzinfo=FixedOffset(dictionary['__tzshift__']))
        return res

    return dictionary
