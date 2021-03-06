from django.urls import path

from box_integration.views import (
    box_get_authorization_view,
    box_authorized_view,
    access_token_destroy_view,
)

app_name = "box_integration"
urlpatterns = [
    path("", box_get_authorization_view, name="box_get_authorization_view"),
    path("authorized", box_authorized_view, name="box_authorized_view"),
    path("destroy", access_token_destroy_view, name="access_token_destroy_view"),
]
