
Overview
--------
Copied from https://github.com/lpm0073/edx-oauth2-wordpress-backend

TODO



Usage
-----


1. add this package to your project's requiremets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



3. configure your Open edX lms application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: yaml

  ADDL_INSTALLED_APPS:
  - "auth0_oauth2"
  THIRD_PARTY_AUTH_BACKENDS:
  - "auth0_oauth2.auth0.Auth0OAuth2"
  ENABLE_REQUIRE_THIRD_PARTY_AUTH: true


