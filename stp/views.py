from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from stp.forms import BasketItemForm
from stp.models import Campaign, Item, BasketItem


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'stp/index_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["campaign_set"] = Campaign.objects.all().order_by("pk")
        return context


class DetailView(LoginRequiredMixin, TemplateView):
    template_name = "stp/detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        campaign = Campaign.objects.get(pk=kwargs["pk"])
        context["campaign"] = campaign
        item_set = Item.objects.filter(campaign=context["campaign"]).order_by("id")
        context["item_set"] = item_set
        BasketItemFormSet = modelformset_factory(BasketItem, extra=item_set.count(), form=BasketItemForm)
        basket_item_form_set = BasketItemFormSet()
        context["basket_item_form_set"] = basket_item_form_set

        return context

    def post(self, *args, **kwargs):
        return HttpResponseRedirect(redirect_to=reverse("index"))
