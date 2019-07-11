from django.db import models


def get_or_create_item():
    item, _ = Item.objects.get_or_create(name="no item")
    return item.pk


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
