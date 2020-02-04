from django.db import models
from django.contrib.auth.models import User
from units.models import Unit


# Create your models here.
class Basket(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	@staticmethod
	def get_basket(basket_user):
		if type(basket_user) is not User:
			raise ValueError("only django.contrib.auth.models.User accepted")
		baskets = Basket.objects.filter(user=basket_user)
		if len(baskets) == 0:
			new_basket = Basket.objects.create(user=basket_user)
			return new_basket
		elif len(baskets) == 1:
			return baskets[0]
		else:  # есть какие-то левые  несколько корзин
			# удаление всех старых
			baskets.delete()
			# и создание новой (кашерной)
			new_basket = Basket.objects.create(user=basket_user)
			return new_basket


class BasketUnit(models.Model):
	basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
