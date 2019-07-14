from numbers import Number

from django.test import TestCase, Client
from django.urls import reverse

from stp.models import BasketItem, Item, Order, Dealer, Packet, Campaign
from users.models import User


class StpLoginTest(TestCase):
    def setUp(self):
        self.testuser_username = "testuser_username"
        self.testuser_password = "testuser_password"
        self.testuser_email = "testuser@example.com"

        self.testuser = User.objects.create_user(
            username=self.testuser_username,
            email=self.testuser_email,
        )
        self.testuser.set_password(self.testuser_password)
        self.testuser.save()

        # ログインしていない場合のURLとtemplateの対応
        self.not_authenticated_correspondence = [
            {'url': '/', 'template_name': 'registration/login.html'},
        ]
        # ログインしている場合のURLとtemplateの対応
        self.authenticated_correspondence = [
            {'url': '/', 'template_name': 'stp/index_view.html'},
        ]
        self.logged_in = self.client.login(
            username=self.testuser_username,
            password=self.testuser_password,
        )

    def test_logged_in(self):
        self.assertTrue(self.logged_in)

    # ログインしていないユーザーにはURLに対応するtemplateを返す
    def test_templates_for_not_authenticated_user(self):
        logged_in = self.client.logout()
        # ログインしていないことを確認
        self.assertFalse(logged_in)

        # URLにあったtemplateを返すことを確認
        for c in self.not_authenticated_correspondence:
            response = self.client.get(c["url"], follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name=c["template_name"])

    # ログインしているユーザーにURLに対応するtemplateを返す
    def test_templates_for_authenticated_user(self):
        # URLにあったtemplateを返すことを確認
        for c in self.authenticated_correspondence:
            response = self.client.get(c["url"], follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name=c["template_name"])

    # # ログイン画面で正しいIDとパスワードを入力すると正しい内容のPOSTが飛ぶ
    # # ログイン画面で誤ったIDとパスワードを入力するとエラーメッセージが表示される
    # # → Django側ですでにテストされているので不要


class StpViewTest(TestCase):
    pass


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

    # Dealer に要素を一つ追加したら、カウントは１増加
    def test_dealer_is_not_empty(self):
        before_save_count = Dealer.objects.all().count()
        dealer = Dealer()
        dealer.save()
        dealers = Dealer.objects.all()
        self.assertEqual(dealers.count() - before_save_count, 1)

    # Item に要素を一つ追加したら、カウントは１増加
    def test_item_is_not_empty(self):
        before_save_count = Item.objects.all().count()
        item = Item()
        item.save()
        items = Item.objects.all()
        self.assertEqual(items.count() - before_save_count, 1)

    # Packet に要素を一つ追加したら、カウントは１増加
    def test_packet_is_not_empty(self):
        before_save_count = Packet.objects.all().count()
        packet = Packet()
        packet.save()
        packets = Packet.objects.all()
        self.assertEqual(packets.count() - before_save_count, 1)

    # Campaign に要素を一つ追加したら、カウントは１増加
    def test_campaign_is_not_empty(self):
        before_save_count = Campaign.objects.all().count()
        campaign = Campaign()
        campaign.save()
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
