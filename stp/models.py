from django.db import models

from users.models import User


def get_or_create_item():
    item, _ = Item.objects.get_or_create(name="null item")
    return item.pk


def get_or_create_order():
    order, _ = Order.objects.get_or_create(pk=1)
    return order.pk


def get_or_create_user():
    user, _ = User.objects.get_or_create(pk=1)
    return user.pk


class Item(models.Model):
    name = models.CharField(
        max_length=100,
        null=True,
    )


class BasketItem(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        default=get_or_create_item,
    )
    nos = models.IntegerField(
        default=0,
    )
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        default=get_or_create_order,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=get_or_create_user,
    )


class Order(models.Model):
    pass


class Dealer(models.Model):
    pass


class Packet(models.Model):
    pass


class Campaign(models.Model):
    pass
