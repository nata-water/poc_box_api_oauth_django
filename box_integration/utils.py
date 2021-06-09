from boxsdk import OAuth2
from django.shortcuts import get_object_or_404

from box_integration.models import BoxConfig
from my_box_project.settings import APP_ENVIRONMENT


def factory_oauth_instance(request):
    box_config = get_object_or_404(BoxConfig, app_environment=APP_ENVIRONMENT)
    access_token = ""
    if "access_token" in request.session:
        access_token = request.session["access_token"]

    refresh_token = ""
    if "refresh_token" in request.session:
        refresh_token = request.session["refresh_token"]

    print(f"factory_oauth_instance: {access_token}")
    oauth = OAuth2(
        client_id=box_config.app_client_id,
        client_secret=box_config.app_secret,
        # store_tokens=store_tokens,
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return oauth


def store_tokens(access_token, refresh_token):
    print(f"store_tokensです {access_token}  _   {refresh_token}")
