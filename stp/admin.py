from django.contrib import admin
from django.contrib.admin import ModelAdmin

from stp.models import Campaign


@admin.register(Campaign)
class CampaignAdmin(ModelAdmin):
    pass
