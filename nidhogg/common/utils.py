from uuid import uuid1


def generate_token():
    """Generate random UUID token like Java's UUID.toString()

    :rtype: str
    """
    return uuid1().hex
