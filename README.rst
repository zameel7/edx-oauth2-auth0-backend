
Overview
--------
Copied from https://github.com/lpm0073/edx-oauth2-wordpress-backend


Usage
-----


1. add this package to your project's requiremets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add this project to requirements.
Also add `python-jose==3.0.0` since it is not being picked up from the project's requirements.

Your private.txt should looke like this at the end:

..  code-block:: yaml

  -e ./edx-oauth2-auth0-backend/
  python-jose==3.0.0


2. configure your Open edX lms application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: yaml

  ADDL_INSTALLED_APPS:
  - "auth0_oauth2"
  THIRD_PARTY_AUTH_BACKENDS:
  - "auth0_oauth2.auth0.Auth0OAuth2"
  ENABLE_REQUIRE_THIRD_PARTY_AUTH: true


