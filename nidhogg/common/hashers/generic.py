def check_password(raw=None, hash=None):
    return raw == hash


def set_password(raw=None):
    return raw