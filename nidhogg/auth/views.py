from pyramid.view import view_defaults
from pyramid.view import view_config

from nidhogg.auth.resources import AuthEndpoint
from nidhogg.auth import schemas
from nidhogg.auth import logic as bl


@view_defaults(request_method="POST", context=AuthEndpoint, renderer='json')
class YggdrasilAuthViews:
    """Class-based view as wrapper for HTTP API"""

    SCHEMA_ROUTER = {
        "authenticate": schemas.Authenticate,
        "refresh": schemas.Refresh,
        "validate": schemas.AccessToken,
        "signout": schemas.Credentials,
        "invalidate": schemas.TokensPair
    }

    def __init__(self, request, context):
        self.request = request
        self.context = context
        current_schema = self.SCHEMA_ROUTER[request.view_name]
        self.payload = current_schema().deserialize(self.request.json_body)

    @view_config()
    def authenticate(self):
        """Authenticate endpoint

        :rtype: dict
        :return: Result dictionary
        """
        user = bl.get_user(self.payload["username"], self.payload["password"])
        token = bl.authenticate_user(user, self.payload["clientToken"])
        profile = {"id": token.client, "name": user.login}

        return {
            "accessToken": token.access,
            "clientToken": token.client,
            "selectedProfile": profile,
            "availableProfiles": [profile],
            "agent": schemas.AGENT,
        }

    @view_config()
    def refresh(self):
        """Refresh endpoint

        :rtype: dict
        :return: Result dictionary
        """
        token = bl.get_token(self.payload["clientToken"])
        fresh_token = bl.refresh_token(token)
        return fresh_token.as_dict()

    @view_config()
    def validate(self):
        """Validate endpoint"""
        bl.validate_token(self.payload["accessToken"])

    @view_config()
    def signout(self):
        """Signout endpoint

        Invalidate token using an account's username and password
        """
        user = bl.get_user(self.payload["username"], self.payload["password"])
        bl.invalidate_token(user.token)

    @view_config()
    def invalidate(self):
        """Invalidates accessTokens using a client/access token pair"""
        token = bl.get_token(self.payload["clientToken"])
        bl.invalidate_token(token)
