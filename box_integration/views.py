from boxsdk import Client
from django import views
from django.shortcuts import redirect, render

from box_integration import utils
from my_box_project import settings


class BoxGetAuthorizationView(views.View):
    def get(self, *args, **kwargs):

        oauth = utils.factory_oauth_instance(self.request)
        auth_url, csrf_token = oauth.get_authorization_url(settings.APP_REDIRECT_URL)

        return redirect(auth_url)


class BoxAuthorizedView(views.View):
    def get(self, *args, **kwargs):

        code = self.request.GET["code"]
        print(code)

        oauth = utils.factory_oauth_instance(self.request)
        access_token, refresh_token = oauth.authenticate(code)

        self.request.session["access_token"] = access_token
        self.request.session["refresh_token"] = refresh_token

        print(f"セッション.アクセストークン: {self.request.session['access_token']}")
        client = Client(oauth)
        print(f"client.user.get(): {client.user().get()}")
        print(f"アクセストークン:{access_token} リフレッシュトークン{refresh_token}")
        return render(self.request, "box_integration/base.html", {})


box_get_authorization_view = BoxGetAuthorizationView.as_view()
box_authorized_view = BoxAuthorizedView.as_view()
