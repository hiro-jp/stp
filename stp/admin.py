from django.contrib import admin
from django.contrib.admin import ModelAdmin

from stp.models import Campaign, BasketItem, Item, Order


@admin.register(Campaign)
class CampaignAdmin(ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    pass


@admin.register(BasketItem)
class BasketItemAdmin(ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    pass


