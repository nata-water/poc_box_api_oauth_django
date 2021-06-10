from boxsdk import OAuth2
from django.shortcuts import get_object_or_404

from box_integration.models import BoxConfig
from my_box_project.settings import APP_ENVIRONMENT


def get_session_value(request, key):
    value = ""
    if key in request.session:
        value = request.session[key]
    return value


def store_tokens(access_token, refresh_token):
    print(f"store_tokensです {access_token}  _   {refresh_token}")
