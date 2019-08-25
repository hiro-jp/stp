from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView
from stp.forms import ItemInlineFormset, BasketItemModelFormset, OrderCreateForm, OrderDispatchForm
from stp.models import Campaign, Item, BasketItem, Order


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "stp/index.html"


class CampaignListView(LoginRequiredMixin, TemplateView):
    template_name = 'stp/campaign_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["campaign_set"] = Campaign.objects.all().order_by("pk")
        return context


def email_order_placed(request, order: Order, basket_item_set: QuerySet):
    subject = "ご注文の確認"
    template = "stp/email_order_placed.html"
    context = {
        'order': order,
        'basket_item_set': basket_item_set,
    }
    message = render_to_string(template, context, request)

    from_email = 'teitoku_2ch@yahoo.co.jp'
    recipient_email = {'hiroyuki.wx@gmail.com'}

    send_mail(subject, message, from_email, recipient_email)


def email_auto_approval(request, order: Order, basket_item_set: QuerySet):
    subject = "自動承認完了通知"
    template = "stp/email_auto_approval.html"
    context = {
        'order': order,
        'basket_item_set': basket_item_set,
    }
    message = render_to_string(template, context, request)

    from_email = 'teitoku_2ch@yahoo.co.jp'
    recipient_email = {'hiroyuki.wx@gmail.com'}

    send_mail(subject, message, from_email, recipient_email)


# 設計上は approved だが、事実上は発送業者にオーダー到着を連絡するメール
def email_approved(request, order: Order, basket_item_set: QuerySet):
    subject = "オーダー到着通知"
    template = "stp/email_approved.html"
    context = {
        'order': order,
        'basket_item_set': basket_item_set,
    }
    message = render_to_string(template, context, request)

    from_email = 'teitoku_2ch@yahoo.co.jp'
    recipient_email = {'hiroyuki.wx@gmail.com'}

    send_mail(subject, message, from_email, recipient_email)


def email_order_dispatched(request, order: Order, basket_item_set: QuerySet):
    subject = "発送のお知らせ"
    template = "stp/email_dispatched.html"
    context = {
        'order': order,
        'basket_item_set': basket_item_set,
    }
    message = render_to_string(template, context, request)

    from_email = 'teitoku_2ch@yahoo.co.jp'
    recipient_email = {'hiroyuki.wx@gmail.com'}

    send_mail(subject, message, from_email, recipient_email)


def email_completed(request, order: Order, basket_item_set: QuerySet):
    subject = "発送完了通知"
    template = "stp/email_completed.html"
    context = {
        'order': order,
        'basket_item_set': basket_item_set,
    }
    message = render_to_string(template, context, request)

    from_email = 'teitoku_2ch@yahoo.co.jp'
    recipient_email = {'hiroyuki.wx@gmail.com'}

    send_mail(subject, message, from_email, recipient_email)


@login_required
def order_create_view(request, pk):
    basket_item_set = BasketItem.objects.filter(user=request.user, item__campaign_id=pk, order=None)
    if basket_item_set.count() == 0:
        raise Http404

    item_set = Item.objects.filter(basketitem__in=basket_item_set)

    campaign = get_object_or_404(Campaign, pk=pk)
    order = Order.objects.get_or_create(order_user=request.user, campaign=campaign, is_placed=False)[0]
    dealer = request.user.dealer

    # 宛先初期値に所属するDealerのものをコピー
    order.dealer_name = dealer.name
    order.zip_code = dealer.zip_code
    order.address = dealer.address
    order.telephone = dealer.telephone
    order.recipient = dealer.recipient

    order_form = OrderCreateForm(request.POST or None, instance=order)
    template = "stp/order_create_view.html"

    if request.method == 'POST' and order_form.is_valid():
        for basket_item in basket_item_set:
            basket_item.order = order
            basket_item.save()

        order_form_instance = order_form.instance

        if order.campaign.is_auto_approvable(basket_item_set):
            order_form_instance.is_approved = True
            email_auto_approval(request, order, basket_item_set)
            email_approved(request, order, basket_item_set)

        order_form_instance.is_placed = True
        order_form_instance.date_placed = timezone.datetime.now()

        if order_form.cleaned_data['apply_zip_address']:
            dealer.zip_code = order_form_instance.zip_code
            dealer.address = order_form_instance.address
        if order_form.cleaned_data['apply_telephone']:
            dealer.telephone = order_form_instance.telephone
        if order_form.cleaned_data['apply_recipient']:
            dealer.recipient = order_form_instance.recipient

        dealer.save()
        order_form.save()

        email_order_placed(request, order, basket_item_set)

        return redirect('order_list')

    context = {
        "basket_item_set": basket_item_set,
        "form": order_form,
        "item_set": item_set,
        "campaign": campaign,
        "is_order_create": True,
    }
    return render(request, template_name=template, context=context)


class OrderApproveListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "stp/order_list_view.html"

    def get_queryset(self):
        queryset = Order.objects.filter(campaign__approver=self.request.user).filter(is_approved=False)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['is_approve_list'] = True
        return context


@login_required
def order_approve_view(request, pk):
    template = "stp/order_approve_view.html"
    order = get_object_or_404(Order, pk=pk)
    basket_item_set = BasketItem.objects.filter(order=order)
    item_set = Item.objects.filter(basketitem__in=basket_item_set)

    if request.method == 'POST':
        order.is_approved = True
        order.date_approved = timezone.datetime.now()
        email_approved(request, order, basket_item_set)
        order.save()
        return redirect('order_approve_list')

    context = {
        "order": order,
        "is_approve": True,
        "basket_item_set": basket_item_set,
        "item_set": item_set
    }

    return render(request, template_name=template, context=context)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "stp/order_list_view.html"

    def get_queryset(self):
        queryset = Order.objects.filter(order_user=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['is_order_list'] = True
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "stp/order_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['basket_item_set'] = BasketItem.objects.filter(order=self.get_object())
        item_set = Item.objects.filter(basketitem__in=context['basket_item_set'])
        context["item_set"] = item_set
        context['is_detail'] = True
        return context


class OrderDispatchListView(ListView):
    model = Order
    template_name = "stp/order_list_view.html"

    def get_queryset(self):
        queryset = Order.objects.filter(is_approved=True, is_dispatched=False)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['is_dispatch_list'] = True
        return context


@login_required
def order_dispatch_view(request, pk):
    template = "stp/order_dispatch_view.html"
    order = get_object_or_404(Order, pk=pk)
    basket_item_set = BasketItem.objects.filter(order=order)
    item_set = Item.objects.filter(basketitem__in=basket_item_set)

    if order.is_dispatched:
        return HttpResponseNotFound()

    form = OrderDispatchForm(request.POST or None, instance=order)

    if request.method == 'POST' and form.is_valid():
        order_form_instance = form.instance
        for basket_item in basket_item_set:
            item = Item.objects.get(basketitem=basket_item)
            item.stock -= basket_item.nos
            item.save()
            email_order_dispatched(request, order, basket_item_set)
            email_completed(request, order, basket_item_set)

        order_form_instance.is_dispatched = True
        order_form_instance.date_dispatched = timezone.datetime.now()
        form.save()
        return redirect('order_dispatch_list')

    context = {
        'form': form,
        'basket_item_set': basket_item_set,
        'order': order,
        'item_set': item_set,
        'is_dispatch': True,
    }
    return render(request, template, context)


@login_required
def campaign_detail_view(request, pk):
    template = "stp/campaign_detail.html"
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
            if formset.cleaned_data[count]["nos"] is not None:
                basket_item = BasketItem.objects.get_or_create(item=item, user=request.user, order=None)[0]
                basket_item.nos = formset.cleaned_data[count]["nos"]
                basket_item.save()

        return redirect('order_create', pk=campaign.id)

    context = {
        'formset': formset,
        'item_set': item_set,
        'campaign': campaign,
    }
    return render(request, template_name=template, context=context)
