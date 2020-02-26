from django.db import models
from datetime import datetime
from units.models import Unit, UnitPhoto
from django.contrib.auth.models import User
from account.models import OftyUser
import pytz


# Create your models here.
class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_owner')  # хозяин товаров в сделке
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_client')  # клиент (инициатор сделки)
    status = models.TextField(default="init")
    commentary = models.TextField(default="")
    start_date = models.DateTimeField(default=datetime(1970, 1, 1, tzinfo=pytz.UTC))
    stop_date = models.DateTimeField(default=datetime(1970, 1, 2, tzinfo=pytz.UTC))
    bail = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    is_deleted = False  # удаление

    def owner_info(self):
        ui = OftyUser.objects.get(user=self.owner, is_deleted=False)
        ans = {
            "name": ui.nickname if ui.nickname != '' else self.owner.username,
            "phone": ui.phone,
            "phone2": ui.phone2
        }
        return ans

    def client_info(self):
        ui = OftyUser.objects.get(user=self.client, is_deleted=False)
        ans = {
            "name": ui.nickname if ui.nickname != '' else self.owner.username,
            "phone": ui.phone,
            "phone2": ui.phone2
        }
        return ans

    def get_photos(self, request):
        # получить набор фотографий товаров (по одной фотке за каждый)
        order_photos = list()
        units = OrderUnit.objects.filter(order=self)
        for ou in units:
            try:
                temp = UnitPhoto.get_unit_photos(ou.unit, request)
                if len(temp) > 0:
                    order_photos.append(request.build_absolute_uri(temp[0]))
            except Unit.DoesNotExist:
                order_photos.append(request.build_absolute_uri('/static/img/shared/no_img.png'))
        return order_photos

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
            "history": "в архиве",
        }
        if status in translate:
            return translate[status]
        else:
            return "status error"


class OrderUnit(models.Model):
    """ товар, входящий в сделку order """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
