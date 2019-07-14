from numbers import Number

from django.test import TestCase, Client
from django.urls import reverse

from stp.models import BasketItem, Item, Order, Dealer, Packet, Campaign
from users.models import User


# ログイン状態でテストするためのスーパークラス
# 以降、ログイン状態でテストしたい場合はこれを継承する
class StpLoggedInTestCase(TestCase):
    fixtures = [
        'stp/campaign_fixture',
        'stp/item_fixture',
    ]

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
            {'url': reverse("index"), 'template_name': 'registration/login.html'},
        ]
        # ログインしている場合のURLとtemplateの対応
        self.authenticated_correspondence = [
            {'url': reverse("index"), 'template_name': 'stp/index_view.html'},
        ]
        self.logged_in = self.client.login(
            username=self.testuser_username,
            password=self.testuser_password,
        )


class LoginAndLogoutTest(StpLoggedInTestCase):
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


class StpIndexViewTest(StpLoggedInTestCase):
    # index viewのcontextはcampaignのリストを持つ
    def test_context_includes_compaign_set_as_context(self):
        response = self.client.get(reverse("index"))
        context_campaign_set = Campaign.objects.all().order_by("pk")
        self.assertQuerysetEqual(
            response.context["campaign_set"],
            context_campaign_set,
            transform=lambda x: x,  # ''を外す？ようわからん
        )

    # index viewはCampaignのすべてのリストを表示する
    def test_index_view_shows_list_of_campaign(self):
        response = self.client.get(reverse("index"))
        # 正しいtemplateを使う
        self.assertTemplateUsed(response, "stp/index_view.html")
        for c in Campaign.objects.all():
            self.assertContains(response, c.name)


class StpModelTest(StpLoggedInTestCase):
    # BasketItem はいくつかの要素を持つ
    def test_basket_item_has_some_attributes(self):
        basket_item = BasketItem()
        basket_item.save()
        first_basket_item = BasketItem.objects.first()
        self.assertIsInstance(first_basket_item.order, Order)
        self.assertIsInstance(first_basket_item.item, Item)
        self.assertIsInstance(first_basket_item.nos, Number)
        self.assertIsInstance(first_basket_item.user, User)

    # Campaign はいくつかの要素を持つ
    def test_campaign_has_some_attributes(self):
        campaign = Campaign.objects.first()
        self.assertIsInstance(campaign.name, str)

    # Campaign から Item を逆参照できる
    def test_campaign_inverse_refer_item_set(self):
        campaign = Campaign.objects.get(pk=1)
        self.assertQuerysetEqual(
            campaign.item_set.all().order_by("pk"),
            Item.objects.filter(campaign=campaign).order_by("pk"),
            transform=lambda x: x,
        )
