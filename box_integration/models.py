from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone


class AppUser(AbstractUser):
    """アプリユーザ
    setting.pyのAUTH_USER_MODELを指定することで拡張する
    さらに拡張性を求める場合はAbstractBaseUserを継承する
    """

    class Meta:
        db_table = "app_user"

    email = models.EmailField(null=True, blank=True)
    refresh_token = models.CharField(max_length=500, null=True, blank=True)
    last_authorized_dt = models.DateTimeField(auto_now=True)
    box_user_id = models.CharField(max_length=50, null=True, blank=True)
    create_dt = models.DateTimeField(default=timezone.now)
    update_dt = models.DateTimeField(auto_now=True)


class BoxConfig(models.Model):
    class Meta:
        db_table = "box_config"

    app_environment = models.CharField(max_length=50)
    app_client_id = models.CharField(max_length=255)
    app_secret = models.CharField(max_length=255)
    create_dt = models.DateTimeField(default=timezone.now)
    update_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.app_environment
