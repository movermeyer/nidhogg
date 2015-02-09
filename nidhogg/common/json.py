from datetime import date, time, datetime

from nidhogg.common.utils import FixedOffset


def json_datetime_hook(dictionary):
    """JSON object_hook function for decoding date/time/datetime objects.
    Usage: json.loads(object, object_hook=json_datetime_hook)

    :type dictionary: dict[str, list[int]]
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
