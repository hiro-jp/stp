from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

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
        context["campaign"] = Campaign.objects.get(pk=kwargs["pk"])
        basket_item = BasketItem()
        context["item_set"] = Item.objects.filter(campaign=context["campaign"]).order_by("id")
        return context

    def post(self, *args, **kwargs):
        return HttpResponseRedirect(redirect_to=reverse("index"))
