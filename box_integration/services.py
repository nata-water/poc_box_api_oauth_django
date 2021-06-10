from django.utils import timezone
from box_integration import api
from box_integration.models import AppUser
from box_integration.utils import get_session_value


def validate_self_app_user(request, oauth):
    user = api.get_oauth_user(oauth)
    # user.login: メールアドレスが格納されている
    # user.name: 氏名
    # user.phone: 電話番号
    # user.id: BoxのユーザID
    box_user_id = user.id
    name = user.name
    email = user.login
    phone = user.phone

    # ユーザが存在しない場合
    app_user = AppUser.objects.filter(email=email)
    if not app_user.exists():
        app_user = AppUser()
        app_user.email = email
        app_user.username = email
        app_user.box_user_id = box_user_id
        app_user.refresh_token = get_session_value(
            request, api.SESSION_KEY_REFRESH_TOKEN
        )
        app_user.last_authorized_dt = timezone.now()
        app_user.save()
    else:
        current_user = app_user.get()
        current_user.refresh_token = get_session_value(
            request, api.SESSION_KEY_REFRESH_TOKEN
        )
        current_user.last_authorized_dt = timezone.now()
        current_user.save()
    print(f"ユーザインスタンス: {user}")
