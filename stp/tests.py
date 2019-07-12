from numbers import Number

from django.test import TestCase
from django.urls import reverse

from stp.models import BasketItem, Item, Order, Dealer, Packet, Campaign
from users.models import User


class StpViewTest(TestCase):
    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, "Hello world!")


class StpModelTest(TestCase):
    # BasketItem に要素を一つ追加したら、カウントは１
    def test_basket_item_is_not_empty(self):
        before_save_count = BasketItem.objects.all().count()
        basket_item = BasketItem()
        basket_item.save()
        saved_basket_items = BasketItem.objects.all()
        self.assertEqual(saved_basket_items.count() - before_save_count, 1)

    # Order に要素を一つ追加したら、カウントは１増加
    def test_order_is_not_empty(self):
        before_save_count = Order.objects.all().count()
        order = Order()
        order.save()
        orders = Order.objects.all()
        self.assertEqual(orders.count() - before_save_count, 1)

    # Dealer に要素を一つ追加したら、カウントは１
    def test_dealer_is_not_empty(self):
        before_save_count = Dealer.objects.all().count()
        dealer = Dealer()
        dealer.save()
        dealers = Dealer.objects.all()
        self.assertEqual(dealers.count() - before_save_count, 1)

    # Item に要素を一つ追加したら、カウントは１
    def test_item_is_not_empty(self):
        before_save_count = Item.objects.all().count()
        item = Item()
        item.save()
        items = Item.objects.all()
        self.assertEqual(items.count() - before_save_count, 1)

    # Packet に要素を一つ追加したら、カウントは１
    def test_packet_is_not_empty(self):
        before_save_count = Packet.objects.all().count()
        packet = Packet()
        packet.save()
        packets = Packet.objects.all()
        self.assertEqual(packets.count() - before_save_count, 1)

    # Campaign に要素を一つ追加したら、カウントは１
    def test_campaign_is_not_empty(self):
        before_save_count = Campaign.objects.all().count()
        campaign = Campaign()
        campaign.sage()
        campaigns = Campaign.objects.all()
        self.assertEqual(campaigns.count() - before_save_count, 1)

    # BasketItem はいくつかの要素を持つ
    def test_basket_item_has_some_attributes(self):
        basket_item = BasketItem()
        basket_item.save()
        first_basket_item = BasketItem.objects.first()
        self.assertIsInstance(first_basket_item.item, Item)
        self.assertIsInstance(first_basket_item.nos, Number)
        self.assertIsInstance(first_basket_item.order, Order)
        self.assertIsInstance(first_basket_item.user, User)