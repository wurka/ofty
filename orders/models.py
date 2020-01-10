from django.db import models
from datetime import datetime
from units.models import Unit
from django.contrib.auth.models import User


# Create your models here.
class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_owner')  # хозяин товаров в сделке
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_client')  # клиент (инициатор сделки)
    status = models.TextField(default="init")
    commentary = models.TextField(default="")
    start_date = models.DateTimeField(default=datetime(1970, 1, 1))
    stop_date = models.DateTimeField(default=datetime(1970, 1, 2))
    bail = models.FloatField(default=0)
    cost = models.FloatField(default=0)

    @staticmethod
    def get_status_text(status):
        """ получение текста СТАТУС """
        translate = {
            "init": "новый заказ",
            "rejected-by-owner": "отклонён владельцем",
            "rejected-by-client": "отменена Вами",
            "tuned-by-owner": "ждёт Вашего согласования",
            "tuned-by-client": "ожидание согласования с владельцем",
            "wait": "согласовано",
            "active": "активна",
        }
        if status in translate:
            return translate[status]
        else:
            return "status error"


class OrderUnit(models.Model):
    """ товар, входящий в сделку order """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
