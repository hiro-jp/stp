from django import forms
from django.core import validators
from django.forms import ModelForm, Textarea, NumberInput, BaseFormSet, modelformset_factory, inlineformset_factory

from stp.models import BasketItem, Item, Campaign, Order
from users.models import User


class BasketItemForm(ModelForm):
    class Meta:
        model = BasketItem
        fields = ['nos']
        widgets = {'nos': NumberInput(attrs={'min': 0})}


class ItemForm(ModelForm):
    nos = forms.IntegerField(validators=[validators.MinValueValidator(0)], required=False, min_value=0)

    class Meta:
        model = Item
        fields = {}


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['address']


ItemInlineFormset = inlineformset_factory(Campaign, Item, form=ItemForm, extra=0)

ItemModelFormset = modelformset_factory(Item, form=ItemForm, extra=0)

BasketItemModelFormset = modelformset_factory(BasketItem, form=BasketItemForm, extra=0)
