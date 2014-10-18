from datetime import timedelta, tzinfo
import uuid


def generate_token():
    """Generate random UUID token like Java's UUID.toString()

    :rtype: str
    """
    return uuid.uuid1().hex


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


class Classproperty(property):
    """Property decorator for classes."""

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()
