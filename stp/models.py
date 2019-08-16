from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import QuerySet


class Dealer(models.Model):
    name = models.CharField(
        max_length=30,
        default="no name",
    )
    abb_name = models.CharField(
        max_length=10,
        default="no abb_name",
    )
    dealer_code = models.CharField(
        max_length=5,
        default="00000",
    )
    zip_code = models.CharField(
        max_length=7,
        default="0000000",
    )
    address = models.CharField(
        max_length=100,
        default="no address",
    )
    telephone = models.CharField(
        max_length=11,
        default="00000000000",
    )
    recipient = models.CharField(
        max_length=20,
        default="no recipient",
    )


from users.models import User


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
    stock = models.IntegerField(
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
        null=True,
        blank=True,
    )


class Order(models.Model):
    order_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_approved = models.BooleanField(
        default=False,
    )

    is_dispatched = models.BooleanField(
        default=False,
    )
    tracking_number = models.CharField(
        max_length=20,
        null=True,
        blank=False,
    )
    campaign = models.ForeignKey(
        'Campaign',
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    is_placed = models.BooleanField(
        default=False,
    )
    dealer_name = models.CharField(
        max_length=30,
        default="no name",
    )
    zip_code = models.CharField(
        max_length=7,
        default="0000000",
    )
    address = models.CharField(
        max_length=100,
        default="no address",
    )
    telephone = models.CharField(
        max_length=11,
        default="00000000000",
    )
    recipient = models.CharField(
        max_length=20,
        default="no recipient",
    )
    date_placed = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
    )
    date_approved = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
    )
    date_dispatched = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
    )


class Campaign(models.Model):
    name = models.CharField(
        max_length=100,
        default="no name",
    )
    approver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def is_auto_approvable(self, basket_item_set: QuerySet):
        result = True
        for basket_item in basket_item_set:
            item = Item.objects.get(basketitem=basket_item)
            if item.thresh_auto_app < basket_item.nos:
                result = result and False
        return result
