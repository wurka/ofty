from django.db import models


# Create your models here.
class City(models.Model):
	name = models.TextField(default="")
