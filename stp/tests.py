from numbers import Number

from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse

from selenium import webdriver

from stp.models import BasketItem, Item, Order, Dealer, Packet, Campaign
from users.models import User


# ログイン状態でテストするためのスーパークラス
# 以降、ログイン状態でテストしたい場合はこれを継承する
class StpLoggedInTestCase(TestCase):
    fixtures = [
        'stp/user_fixture',
        'stp/order_fixture',
        'stp/campaign_fixture',
        'stp/item_fixture',
        'stp/basket_item_fixture'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testuser_username = "testuser_username"
        cls.testuser_password = "testuser_password"
        cls.testuser_email = "testuser@example.com"

        cls.testuser = User.objects.create_user(
            username=cls.testuser_username,
            email=cls.testuser_email,
        )
        cls.testuser.set_password(cls.testuser_password)
        cls.testuser.save()

        # ログインしていない場合のURLとtemplateの対応
        cls.not_authenticated_correspondence = [
            {'url': reverse("index"), 'template_name': 'registration/login.html'},
        ]
        # ログインしている場合のURLとtemplateの対応
        cls.authenticated_correspondence = [
            {'url': reverse("index"), 'template_name': 'stp/index_view.html'},
        ]

    def setUp(self):
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


class SeleniumLoggedInTestCase(LiveServerTestCase):
    fixtures = [
        'stp/user_fixture',
        'stp/order_fixture',
        'stp/campaign_fixture',
        'stp/item_fixture',
        'stp/basket_item_fixture'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testuser_username = "testuser_username"
        cls.testuser_password = "testuser_password"
        cls.browser = webdriver.Chrome()
        cls.browser.get("http://127.0.0.1:8000/")
        input_username = cls.browser.find_element_by_id('id_username')
        input_username.send_keys(cls.testuser_username)
        input_password = cls.browser.find_element_by_id('id_password')
        input_password.send_keys(cls.testuser_password)
        cls.browser.find_element_by_class_name("submit").click()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()


class StpTemplateTest(SeleniumLoggedInTestCase):
    def test_index_template_click_on_certain_link(self):
        self.browser.get("http://127.0.0.1:8000/")
        self.browser.find_element_by_id('stp_detail_1').click()
        current_url = self.browser.current_url
        self.assertEqual("http://127.0.0.1:8000/detail/1", current_url)


class StpIndexViewTest(StpLoggedInTestCase):
    # index viewのcontextはすべてのcampaignのリストを持つ
    def test_context_includes_compaign_set(self):
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


class StpDetailViewTest(StpLoggedInTestCase):
    # detail viewのcontextはCampaignの詳細を持つ
    # detail viewのcontextはCampaignに紐づくitemのリストをもつ
    def test_context_includes_campaign_and_item_detail(self):
        response = self.client.get(reverse("detail", kwargs={'pk': 1}))
        context_campaign = Campaign.objects.get(pk=1)
        self.assertEqual(
            response.context["campaign"],
            context_campaign,
        )
        context_item_set = Item.objects.filter(campaign=context_campaign).order_by("id")
        self.assertQuerysetEqual(
            response.context['item_set'],
            context_item_set,
            transform=lambda x: x,
        )

    # detail viewのtemplateはCampaignのdetailとitemのリストを持つ
    def test_detail_view_shows_campaign_detail_and_item_list(self):
        response = self.client.get(reverse("detail", kwargs={'pk': 1}))
        c = Campaign.objects.get(pk=1)
        self.assertTemplateUsed(response, "stp/detail_view.html")
        self.assertContains(response, c.name)
        i = Item.objects.filter(campaign=c)
        for item in i:
            self.assertContains(response, item.name)


class StpModelTest(StpLoggedInTestCase):
    # BasketItem はいくつかの要素を持つ
    def test_basket_item_has_some_attributes(self):
        basket_item = BasketItem.objects.first()
        self.assertIsInstance(basket_item.order, Order)
        self.assertIsInstance(basket_item.item, Item)
        self.assertIsInstance(basket_item.nos, Number)
        self.assertIsInstance(basket_item.user, User)

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

    # Item はいくつかの要素を持つ
    def test_item_model_has_some_attributes(self):
        item = Item.objects.first()
        self.assertIsInstance(item.name, str)
        self.assertIsInstance(item.campaign, Campaign)
        self.assertIsInstance(item.remarks, str)
        self.assertIsInstance(item.incl, Number)
        self.assertIsInstance(item.thresh_auto_app, Number)
        self.assertIsInstance(item.thresh_stock_alert, Number)
