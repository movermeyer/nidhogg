"""Resources for entire project"""

from nidhogg.auth.resources import AuthEndpoint


class Root(dict):
    __name__ = ''
    __parent__ = None


root = Root()
root['auth'] = AuthEndpoint(parent=root)


def root_factory():
    return root