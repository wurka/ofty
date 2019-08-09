from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class OftyUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	badass = models.BooleanField(default=False)
	enable_push = models.BooleanField(default=True)  # мгновенные уведомления
	enable_sound_alert = models.BooleanField(default=True)  # звуковые оповещения
	enable_sms_new_order = models.BooleanField(default=True)  # sms о новом заказе
	enable_sms_startstop = models.BooleanField(default=True)  # sms о начале/конце аренды
	enable_email_new_order = models.BooleanField(default=True)  # сообщение о новом заказе
	enable_email_startstop = models.BooleanField(default=True)  # сообщение о начале/конце аренды

