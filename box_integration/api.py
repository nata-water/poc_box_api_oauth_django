from boxsdk import Client, OAuth2, BoxAPIException
from django.shortcuts import get_object_or_404

from box_integration.models import BoxConfig
from box_integration.utils import get_session_value
from my_box_project.settings import APP_ENVIRONMENT

# セッションキー：アクセストークン
SESSION_KEY_ACCESS_TOKEN = "access_token"
# セッションキー：リフレッシュトークン
SESSION_KEY_REFRESH_TOKEN = "refresh_token"


def get_oauth_user(oauth):
    client = Client(oauth)
    return client.user().get()


def is_authorized_oauth_instance(oauth):
    is_authorized = False
    try:
        user = get_oauth_user(oauth)
        is_authorized = True
        print(user)
    except BoxAPIException:
        print("未認可のユーザです")
    return is_authorized


def factory_oauth_instance(request):
    box_config = get_object_or_404(BoxConfig, app_environment=APP_ENVIRONMENT)
    access_token = get_session_value(request, SESSION_KEY_ACCESS_TOKEN)

    refresh_token = get_session_value(request, SESSION_KEY_REFRESH_TOKEN)
    oauth = OAuth2(
        client_id=box_config.app_client_id,
        client_secret=box_config.app_secret,
        # store_tokens=store_tokens,
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return oauth
