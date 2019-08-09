from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class OftyUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	badass = models.BooleanField(default=False)  # подозрительный пользователь (чмо)
	enable_push = models.BooleanField(default=True)  # мгновенные уведомления
	enable_sound_alert = models.BooleanField(default=True)  # звуковые оповещения
	enable_sms_new_order = models.BooleanField(default=True)  # sms о новом заказе
	enable_sms_startstop = models.BooleanField(default=True)  # sms о начале/конце аренды
	enable_email_new_order = models.BooleanField(default=True)  # сообщение о новом заказе
	enable_email_startstop = models.BooleanField(default=True)  # сообщение о начале/конце аренды
	is_deleted = models.BooleanField(default=False)  # пользователь удалён


class OftyUserRentLord(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	sklad = models.TextField(default="")  # адрес склада
	metro = models.TextField(default="")  # ближайшая станция метро
	commentary = models.TextField(default="")  # комментарий про аренду


class DeliveryCase(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.TextField(default="")  # название метода доставки
	value = models.FloatField(default=0)  # стоимость доставки этим методом
	is_deleted = models.BooleanField(default=False)  # признак удаления
