from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView
from stp.forms import ItemInlineFormset, ItemModelFormset, BasketItemModelFormset, OrderForm
from stp.models import Campaign, Item, BasketItem, Order


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'stp/index_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["campaign_set"] = Campaign.objects.all().order_by("pk")
        return context


# class BasketItemListView(LoginRequiredMixin, ListView):
#     template_name = 'stp/basket_item_list_view.html'
#     model = BasketItem
#
#     def get_queryset(self):
#         queryset = BasketItem.objects.filter(user=self.request.user)
#         return queryset


def edit_view(request):
    template = "stp/detail_view.html"

    basket_item_set = BasketItem.objects.filter(user=request.user)
    item_set = Item.objects.filter(basketitem__user=request.user)
    formset = BasketItemModelFormset(request.POST or None, queryset=basket_item_set)

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        return redirect('edit')

    context = {
        'formset': formset,
        'item_set': item_set,
        # 'campaign': campaign,
    }
    return render(request, template_name=template, context=context)


def order_create_view(request):
    template = "stp/order_view.html"
    basket_item_set = BasketItem.objects.filter(user=request.user)
    order = Order.objects.get_or_create(order_user=request.user)[0]
    form = OrderForm(request.POST or None, instance=order)

    if request.method == 'POST' and form.is_valid():
        for basket_item in basket_item_set:
            basket_item.order = order
            basket_item.save()
        form.save()
        return redirect('index')

    context = {
        "basket_item_set": basket_item_set,
        "form": form,
    }
    return render(request, template_name=template, context=context)


def detail_view(request, pk):
    template = "stp/detail_view.html"
    campaign = get_object_or_404(Campaign, pk=pk)
    formset = ItemInlineFormset(request.POST or None, instance=campaign)
    # ↓ 便利！
    item_set = formset.get_queryset()

    if request.method == 'POST' and formset.is_valid():

        # すでに存在する basket_item ならそれに nos を足す。
        # まだ存在しない basket_item なら新規で作って nos を足す。
        # get_or_create がなぜか tuple で返ってくるので、
        # 末尾に[0]をつけて BasketItem objectにする。
        for count, item in enumerate(item_set):
            if formset.cleaned_data[count]["nos"] is not None and formset.cleaned_data[count]["nos"] > 0:
                basket_item = BasketItem.objects.get_or_create(item=item, user=request.user)[0]
                basket_item.nos += formset.cleaned_data[count]["nos"]
                basket_item.save()

        return redirect('index')

    context = {
        'formset': formset,
        'item_set': item_set,
        'campaign': campaign,
    }
    return render(request, template_name=template, context=context)
