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


class OrderCreateForm(ModelForm):
    apply_zip_address = forms.BooleanField(
        initial=False,
        required=False,
        label="この郵便番号と住所を標準に設定する"
    )
    apply_telephone = forms.BooleanField(
        initial=False,
        required=False,
        label="この電話番号を標準に設定する"
    )
    apply_recipient = forms.BooleanField(
        initial=False,
        required=False,
        label="この受取人を標準に設定する"
    )

    class Meta:
        model = Order
        fields = ['zip_code', 'address', 'telephone', 'recipient']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['style'] = 'width:100%;'


class OrderDispatchForm(ModelForm):
    class Meta:
        model = Order
        fields = ['tracking_number']


ItemInlineFormset = inlineformset_factory(Campaign, Item, form=ItemForm, extra=0)

ItemModelFormset = modelformset_factory(Item, form=ItemForm, extra=0)

BasketItemModelFormset = modelformset_factory(BasketItem, form=BasketItemForm, extra=0)
