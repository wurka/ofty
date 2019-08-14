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
	stock_size = models.IntegerField(default=10)  # рамер склада
	money = models.FloatField(default=0)  # кредитов


class OftyUserRentLord(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	sklad = models.TextField(default="")  # адрес склада
	metro = models.TextField(default="")  # ближайшая станция метро
	commentary = models.TextField(default="")  # комментарий про аренду

	# время работы "сдавателя", понедельник - воскресенье
	mon_enable = models.BooleanField(default=True)
	mon_start_h = models.IntegerField(default=9)
	mon_start_m = models.IntegerField(default=0)
	mon_stop_h = models.IntegerField(default=21)
	mon_stop_m = models.IntegerField(default=0)
	tue_enable = models.BooleanField(default=True)
	tue_start_h = models.IntegerField(default=9)
	tue_start_m = models.IntegerField(default=0)
	tue_stop_h = models.IntegerField(default=21)
	tue_stop_m = models.IntegerField(default=0)
	wed_enable = models.BooleanField(default=True)
	wed_start_h = models.IntegerField(default=9)
	wed_start_m = models.IntegerField(default=0)
	wed_stop_h = models.IntegerField(default=21)
	wed_stop_m = models.IntegerField(default=0)
	thu_enable = models.BooleanField(default=True)
	thu_start_h = models.IntegerField(default=9)
	thu_start_m = models.IntegerField(default=0)
	thu_stop_h = models.IntegerField(default=21)
	thu_stop_m = models.IntegerField(default=0)
	fri_enable = models.BooleanField(default=True)
	fri_start_h = models.IntegerField(default=9)
	fri_start_m = models.IntegerField(default=0)
	fri_stop_h = models.IntegerField(default=21)
	fri_stop_m = models.IntegerField(default=0)
	sat_enable = models.BooleanField(default=False)
	sat_start_h = models.IntegerField(default=9)
	sat_start_m = models.IntegerField(default=0)
	sat_stop_h = models.IntegerField(default=21)
	sat_stop_m = models.IntegerField(default=0)
	sun_enable = models.BooleanField(default=False)
	sun_start_h = models.IntegerField(default=9)
	sun_start_m = models.IntegerField(default=0)
	sun_stop_h = models.IntegerField(default=21)
	sun_stop_m = models.IntegerField(default=0)


class DeliveryCase(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.TextField(default="")  # название метода доставки
	value = models.FloatField(default=0)  # стоимость доставки этим методом
	is_deleted = models.BooleanField(default=False)  # признак удаления
