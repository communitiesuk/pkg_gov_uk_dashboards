"""enable_basic_auth"""

import os
import dash
from flask_basicauth import BasicAuth


def enable_basic_auth(dash_app: dash.Dash):
    """Turn on basic auth for the dash app if required"""
    if os.environ.get("STAGE") == "production":
        if os.environ.get("APP_USERNAME") and os.environ.get("APP_PASSWORD"):
            server = dash_app.server

            # Forcing the auth to prompt on any page if it hasn't already been done.
            server.config["BASIC_AUTH_FORCE"] = True

            server.config["BASIC_AUTH_USERNAME"] = os.environ.get("APP_USERNAME")
            server.config["BASIC_AUTH_PASSWORD"] = os.environ.get("APP_PASSWORD")
            BasicAuth(server)
        else:
            print("failed to set up basic_auth")
