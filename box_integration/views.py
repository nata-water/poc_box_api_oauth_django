from django import views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from box_integration import api, services
from my_box_project import settings

"""
TODO: コンテキストプロセッサーで、各リクエスト処理にアクセストークンの検証処理を差し込む
"""


class BoxGetAuthorizationView(views.View):
    """Boxアプリの認可を検証します。認可済の場合、トップページに移動します"""

    def get(self, *args, **kwargs):
        oauth = api.factory_oauth_instance(self.request)
        is_authorized = api.is_authorized_oauth_instance(oauth)
        if is_authorized:
            print("認可済です")
            return render(self.request, "box_integration/base.html", {})
        else:
            auth_url, csrf_token = oauth.get_authorization_url(
                settings.APP_REDIRECT_URL
            )

            return redirect(auth_url)


class BoxAuthorizedView(views.View):
    """Boxアプリと認可情報の受け渡しを行い、結果を元にアプリ用ユーザの検証を行います"""

    def get(self, *args, **kwargs):
        # 認証コードの受け渡しを行い、アクセストークンを取得する
        code = self.request.GET["code"]
        oauth = api.factory_oauth_instance(self.request)
        access_token, refresh_token = oauth.authenticate(code)

        self.request.session[api.SESSION_KEY_ACCESS_TOKEN] = access_token
        self.request.session[api.SESSION_KEY_REFRESH_TOKEN] = refresh_token

        # Djangoアプリ用のユーザ登録状況を検証する（新規登録 or 最終更新日及びリフレッシュトークン更新)
        services.validate_self_app_user(self.request, oauth)

        return redirect(reverse_lazy("box_integration:box_get_authorization_view"))


class AccessTokenDestroyView(views.View):
    """アクセストークン及びリフレッシュトークンを破棄します"""

    def get(self, *args, **kwargs):
        self.request.session[api.SESSION_KEY_ACCESS_TOKEN] = ""
        self.request.session[api.SESSION_KEY_REFRESH_TOKEN] = ""
        return render(self.request, "box_integration/destroy.html", {})


box_get_authorization_view = BoxGetAuthorizationView.as_view()
box_authorized_view = BoxAuthorizedView.as_view()
access_token_destroy_view = AccessTokenDestroyView.as_view()
