from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView, DetailView
from stp.forms import ItemInlineFormset, ItemModelFormset, BasketItemModelFormset, OrderCreateForm, OrderDispatchForm
from stp.models import Campaign, Item, BasketItem, Order


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'stp/index_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["campaign_set"] = Campaign.objects.all().order_by("pk")
        return context


@login_required
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


@login_required
def order_create_view(request, pk):
    basket_item_set = BasketItem.objects.filter(user=request.user, item__campaign_id=pk, order=None)
    if basket_item_set.count() == 0:
        raise Http404

    order = Order.objects.get_or_create(order_user=request.user, campaign_id=pk, is_placed=False)[0]
    form = OrderCreateForm(request.POST or None, instance=order)
    template = "stp/order_create_view.html"

    if request.method == 'POST' and form.is_valid():
        for basket_item in basket_item_set:
            basket_item.order = order
            basket_item.save()

        instance = form.instance
        if order.campaign.is_auto_approvable(basket_item_set):
            instance.is_approved = True
        instance.is_placed = True
        form.save()
        return redirect('index')

    context = {
        "basket_item_set": basket_item_set,
        "form": form,
    }
    return render(request, template_name=template, context=context)


class OrderApproveListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "stp/order_list_view.html"

    def get_queryset(self):
        queryset = Order.objects.filter(campaign__approver=self.request.user).filter(is_approved=False)
        return queryset


class MyOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "stp/order_list_view.html"

    def get_queryset(self):
        queryset = Order.objects.filter(order_user=self.request.user)
        return queryset


class MyOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "stp/order_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['basket_item_set'] = BasketItem.objects.filter(order=self.get_object())
        return context


@login_required
def order_approve_view(request, pk):
    template = "stp/order_approve_view.html"
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order.is_approved = True
        order.save()
        return redirect('index')

    return render(request, template_name=template)


class OrderDispatchListView(ListView):
    model = Order
    template_name = "stp/order_list_view.html"

    def get_queryset(self):
        queryset = Order.objects.filter(is_approved=True, is_dispatched=False)
        return queryset


@login_required
def order_dispatch_view(request, pk):
    template = "stp/order_dispatch_view.html"
    order = get_object_or_404(Order, pk=pk)
    basket_item_set = BasketItem.objects.filter(order=order)

    form = OrderDispatchForm(request.POST or None, instance=order)

    if request.method == 'POST' and form.is_valid():
        valid_order = form.instance
        valid_order.is_dispatched = True
        form.save()
        return redirect('index')

    context = {
        'form': form,
        'basket_item_set': basket_item_set,
        'order': order,
    }
    return render(request, template, context)


@login_required
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
                basket_item = BasketItem.objects.get_or_create(item=item, user=request.user, order=None)[0]
                basket_item.nos += formset.cleaned_data[count]["nos"]
                basket_item.save()

        return redirect('index')

    context = {
        'formset': formset,
        'item_set': item_set,
        'campaign': campaign,
    }
    return render(request, template_name=template, context=context)

