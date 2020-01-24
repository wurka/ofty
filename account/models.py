from django.db import models
from django.contrib.auth.models import User
from location.models import City
from datetime import datetime


# Create your models here.
class OftyUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	nickname = models.TextField(default="")  # псевдоним пользователя (подпись соощений и т.п.)
	badass = models.BooleanField(default=False)  # подозрительный пользователь (чмо)
	enable_push = models.BooleanField(default=False)  # мгновенные уведомления
	enable_sound_alert = models.BooleanField(default=False)  # звуковые оповещения
	enable_sms_new_order = models.BooleanField(default=False)  # sms о новом заказе
	enable_sms_startstop = models.BooleanField(default=False)  # sms о начале/конце аренды
	enable_email_new_order = models.BooleanField(default=False)  # сообщение о новом заказе
	enable_email_startstop = models.BooleanField(default=False)  # сообщение о начале/конце аренды
	is_deleted = models.BooleanField(default=False)  # пользователь удалён
	stock_size = models.IntegerField(default=10)  # рамер склада
	money = models.FloatField(default=0)  # кредитов
	sklad = models.TextField(default="")  # адрес склада
	metro = models.TextField(default="")  # ближайшая станция метро
	rent_commentary = models.TextField(default="")  # комментарий про аренду
	site = models.URLField(default="")  # адрес сайта
	city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
	email = models.EmailField(default="")
	phone = models.TextField(default="")
	phone2 = models.TextField(default="")
	company_description = models.TextField(default="")  # описание компании
	verification_code = models.BinaryField(default=b'')  # md5 hash кода верификации
	verification_code_until = models.DateTimeField(default=datetime(1970, 1, 1))

	@staticmethod
	def get_user(user):
		# получить OftyUser по обычному пользователю (создать, если не создан)
		try:
			ans = OftyUser.objects.get(user=user)
		except OftyUser.DoesNotExist:
			ans = OftyUser.objects.create()
		return ans


class OftyUserWorkTime(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
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


class BlackListInstance(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")  # хозяин черного списка
	target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="target")  # тот, кто находится в чёрном списке
