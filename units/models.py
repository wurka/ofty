from django.db import models
from datetime import datetime
import pytz
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
import os


# Create your models here.
class Group(models.Model):
	name = models.TextField(default="no name")
	picture = models.TextField(default="group-picture.png")
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		parent = self.parent.name if self.parent is not None else "-"
		return f"name={self.name}, parent={parent}, pic={self.picture}"


class GroupParameter(models.Model):
	owner = models.ForeignKey(Group, on_delete=models.CASCADE)
	name = models.TextField(default="no name")
	dimension = models.TextField(default="")

	def __str__(self):
		return f"{self.name}={self.dimension}"


class Color(models.Model):
	color_group = models.TextField(default="")
	rgb_hex = models.TextField(default="FF00FF")
	texture = models.TextField(default="blank.png")

	def texture_url(self, request):
		# get url of texture (request - for build url)
		if self.texture == "":
			return ""
		else:
			return request.build_absolute_uri("/static/img/units/texture/" + self.texture)


class Material(models.Model):
	name = models.TextField(default="new material")


class Keyword(models.Model):
	name = models.TextField(default="empty key")
	creation_time = models.DateTimeField(default=datetime(1970, 1, 1, tzinfo=pytz.UTC))


class Unit(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # хозяин товара
	weight = models.FloatField(default=0)  # кг, вес
	bail = models.FloatField(default=0)  # рублей, залог
	count = models.FloatField(default=0)  # шт., количество
	title = models.TextField(default="no title")  # заголовок (название)
	first_day_cost = models.FloatField(default=0)  # цена за первый день аренды
	rent_min_days = models.IntegerField(default=0)  # минимальное количество дней аренды
	day_cost = models.FloatField(default=0)  # цена дня аренды
	group = models.ForeignKey(Group, on_delete=models.CASCADE)  # группа товара
	description = models.TextField(default="no description")
	is_deleted = models.BooleanField(default=False)  # True => Элемент удалён
	search_string = models.TextField(default="")  # строка для поиска по ней
	published = models.BooleanField(default=False)  # опубликован ли

	def get_absolute_url(self):
		return reverse('units/unit', args=[str(self.id)])

	def build_search_string(self):
		parent = self.group.parent if self.group is not None else None
		group_text = self.group.name if self.group is not None else ""
		while parent is not None:
			group_text = parent.name + " " + group_text
			parent = parent.parent

		# все ключевые строки через пробел
		kwrd_text = " ".join([x.keyword.name for x in UnitKeyword.objects.filter(unit=self)])

		# строка приводится в нижний регистр, т.к. емучий UTF8 в SQL через жопу LIKE делал
		self.search_string = f"{group_text} {self.description} {self.title} {kwrd_text}".lower()
		self.save()


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

	@staticmethod
	def get_url(user_id, unit_id, photo_number):
		user_id = int(user_id)
		unit_id = int(unit_id)
		photo_number = int(photo_number)
		return f"/static/img/shared/user_{user_id}/unit_{unit_id}/photo{photo_number}.jpg"

	@staticmethod
	def get_unit_photos(unit, request):
		""" получить все фотографии для товара unit"""
		oid = unit.owner.id
		uid = unit.id
		photos = list()

		for i in range(1, 6):
			user_id = unit.owner.id
			img_formats = ['jpg', 'jpeg', 'png']
			for img_format in img_formats:
				photo_path = os.path.join(
					os.getcwd(), 'user_uploads', f'user_{user_id}', f'unit_{unit.id}', f'photo{i}.{img_format}')
				if os.path.exists(photo_path):
					photos.append(  # request.build_absolute_uri(
						f'/static/user_{oid}/unit_{uid}/photo{i}.{img_format}')
					break
		return photos


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
	is_deleted = models.BooleanField(default=False)


class SetElement(models.Model):
	"""
	Один элемент из набора
	"""
	set = models.ForeignKey(Set, on_delete=models.CASCADE)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)


