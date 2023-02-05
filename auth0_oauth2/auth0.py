"""
Auth0 implementation based on:
https://auth0.com/docs/quickstart/webapp/django/01-login
"""
from jose import jwt
import json
from logging import getLogger

from social_core.backends.oauth import BaseOAuth2
from django.contrib.auth import get_user_model

User = get_user_model()
logger = getLogger(__name__)

class BlendEdAuth0OAuth2(BaseOAuth2):
    """Auth0 OAuth authentication backend"""

    # The default key name where the user identification field is defined, it’s
    # used in the auth process when some basic user data is returned. This Id
    # is stored in the UserSocialAuth.uid field and this, together with the
    # UserSocialAuth.provider field, is used to uniquely identify a user association.
    ID_KEY = "email"

    # Flags the backend to enforce email validation during the pipeline
    # (if the corresponding pipeline social_core.pipeline.mail.mail_validation was enabled).
    REQUIRES_EMAIL_VALIDATION = False

    name = "auth0-plugin"
    SCOPE_SEPARATOR = " "
    DEFAULT_SCOPE=["email", "profile", "openid"]
    ACCESS_TOKEN_METHOD = "POST"
    EXTRA_DATA = [("picture", "picture")]
    DOMAIN="blend-ed-dev.us.auth0.com"
    AUDIENCE="6fmZ9A0Z7n3yDKp01N6wLjTu5saclRIz"

    def api_path(self, path=""):
        """Build API path for Auth0 domain"""
        return "https://{domain}/{path}".format(
            domain=self.setting("DOMAIN"), path=path
        )
    def authorization_url(self):
        return self.api_path("authorize")

    def access_token_url(self):
        return self.api_path("oauth/token")

    def get_user_id(self, details, response):
        """Return current user id."""
        logger.warning("Details: {resp}".format(resp=json.dumps(details, sort_keys=True, indent=4)))
        return details["user_id"]

    def get_user_details(self, response):
        # Obtain JWT and the keys to validate the signature
        logger.warning("Response: {resp}".format(resp=json.dumps(response, sort_keys=True, indent=4)))
        
        is_auth_exchange = False

        id_token = response.get("id_token")  
        audience = self.setting("KEY")   
        jwks = self.get_json(self.api_path(".well-known/jwks.json"))
        issuer = self.api_path()

        #if handling an auth_exchange
        if id_token is None: # handling for auth_exchange which doesn't send an id_token
            id_token = response.get("access_token") # attempt to use the access token in this case  
            audience = self.AUDIENCE # match the audience in the access token
            is_auth_exchange = True

        logger.warning(f"-----------------------\nResponse before JWT decode: \nid_token:{id_token} \naudience:{audience} \nissuer:{issuer} \njwks:{jwks} \nis_auth_exchange:{is_auth_exchange}\n---------------------")
        payload = jwt.decode(
            id_token, jwks, algorithms=["RS256"], audience=audience, issuer=issuer
        )

        logger.warning("Payload: {val}".format(val=json.dumps(payload, sort_keys=True, indent=4)))
        if not is_auth_exchange and "email" in payload:
            
            fullname, first_name, last_name = self.get_user_names(payload["name"])
            return {
                "username": payload["nickname"],
                "email": payload["email"],
                "email_verified": payload.get("email_verified", False),
                "fullname": fullname,
                "first_name": first_name,
                "last_name": last_name,
                "picture": payload["picture"],
                "user_id": payload["uid"],
            }
        elif "email" not in payload:
            
            fullname, first_name, last_name = self.get_user_names(payload["name"])
            user_email = f'{payload["name"].strip("+")}@student.blend-ed.com'
            return {
                "username": payload["nickname"],
                "email": user_email,
                "email_verified": payload.get("email_verified", False),
                "fullname": fullname,
                "first_name": first_name,
                "last_name": last_name,
                "picture": payload["picture"],
                "user_id": payload["uid"],
            }
        else:
            # when using an access token, we only have the user_id. We do not have all the other information.
            return {
                "user_id": payload["sub"]
            }
