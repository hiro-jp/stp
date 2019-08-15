from django.core.validators import MinValueValidator
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
    campaign = models.ForeignKey(
        "Campaign",
        on_delete=models.CASCADE,
        related_name="item_set",
        default=1,
    )
    name = models.CharField(
        max_length=100,
        default="no name",
    )
    remarks = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    incl = models.IntegerField(
        default=1,
    )
    thresh_auto_app = models.IntegerField(
        default=0,
    )
    thresh_stock_alert = models.IntegerField(
        default=0,
    )


class BasketItem(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        default=1,
    )
    nos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=get_or_create_user,
    )


class Order(models.Model):
    order_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    address = models.TextField(
        null=True,
    )

    tmc_approved = models.BooleanField(
        default=False,
    )

    dispatched = models.BooleanField(
        default=False,
    )

    tracking_number = models.CharField(
        max_length=20,
        null=True,
    )


class Dealer(models.Model):
    pass


class Packet(models.Model):
    pass


class Campaign(models.Model):
    name = models.CharField(
        max_length=100,
        default="no name",
    )
