from django.db import models
from datetime import datetime
import pytz

# Create your models here.
class Group(models.Model):
	name = models.TextField(default="no name")
	picture = models.TextField(default="group-picture.png")
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)


class GroupParameter(models.Model):
	owner = models.ForeignKey(Group, on_delete=models.CASCADE)
	name = models.TextField(default="no name")
	dimension = models.TextField(default="")


class Color(models.Model):
	color_group = models.TextField(default="")
	rgb_hex = models.TextField(default="FF00FF")
	texture = models.TextField(default="blank.png")


class Material(models.Model):
	name = models.TextField(default="new material")


class Keyword(models.Model):
	name = models.TextField(default="empty key")
	creation_time = models.DateTimeField()


class Unit(models.Model):
	weight = models.FloatField(default=0)  # кг, вес
	bail = models.FloatField(default=0)  # рублей, залог
	count = models.FloatField(default=0)  # шт., количество
	title = models.TextField(default="no title")  # заголовок (название)
	first_day_cost = models.FloatField(default=0)  # цена за первый день аренды
	rent_min_days = models.FloatField(default=0)  # минимальное количество дней аренды
	day_cost = models.FloatField(default=0)  # цена дня аренды
	group = models.ForeignKey(Group, on_delete=models.CASCADE)  # группа товара
	description = models.TextField(default="no description")


class UnitColor(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	color = models.ForeignKey(Color, on_delete=models.CASCADE)


class UnitMaterial(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	material = models.ForeignKey(Material, on_delete=models.CASCADE)


class UnitKeyword(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
	creation_time = models.DateTimeField(default=datetime(1970, 1, 1, tzinfo=pytz.UTC))


class UnitPhoto(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	file_name = models.TextField(default="")


class UnitParameter(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	parameter = models.ForeignKey(GroupParameter, on_delete=models.CASCADE)
	value = models.TextField(default="x")


class Set(models.Model):
	"""
	Коллекция товаров (набор "Всплески радости", например)
	"""
	title = models.TextField(default="empty set title")
	description = models.TextField(default="this set have no description")


class SetElement(models.Model):
	"""
	Один элемент из набора
	"""
	set = models.ForeignKey(Set, on_delete=models.CASCADE)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)


