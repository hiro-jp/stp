from django.forms import ModelForm, Textarea, NumberInput, BaseFormSet, modelformset_factory

from stp.models import BasketItem


class BasketItemForm(ModelForm):
    class Meta:
        model = BasketItem
        fields = ['nos']
        widgets = {'nos': NumberInput(attrs={'min': 0})}
