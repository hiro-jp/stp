from numbers import Number

from django.test import TestCase, Client, LiveServerTestCase, TransactionTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from stp.forms import BasketItemForm
from stp.models import BasketItem, Item, Order, Dealer, Packet, Campaign
from users.models import User


# ログイン状態でテストするためのスーパークラス
# 以降、ログイン状態でテストしたい場合はこれを継承する
class StpLoggedInTestCase(TestCase):
    fixtures = [
        'initial_data'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testuser_username = "testuser_username"
        cls.testuser_password = "testuser_password"

        # ログインしていない場合のURLとtemplateの対応
        cls.not_authenticated_correspondence = [
            {'url': reverse("index"), 'template_name': 'registration/login.html'},
        ]
        # ログインしている場合のURLとtemplateの対応
        cls.authenticated_correspondence = [
            {'url': reverse("index"), 'template_name': 'stp/campaign_list.html'},
        ]

    def setUp(self):
        self.logged_in = self.client.login(
            username=self.testuser_username,
            password=self.testuser_password,
        )


class LoginAndLogoutTest(StpLoggedInTestCase):
    def test_logged_in(self):
        self.client.login(name=self.testuser_username, password=self.testuser_password)
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
        'initial_data'
    ]

    @classmethod
    def setUp(cls):
        super().setUp(cls)
        cls.testuser_username = "testuser_username"
        cls.testuser_password = "testuser_password"
        cls.browser = webdriver.Chrome()
        cls.browser.get(cls.live_server_url)
        input_username = cls.browser.find_element_by_id('id_username')
        input_username.send_keys(cls.testuser_username)
        input_password = cls.browser.find_element_by_id('id_password')
        input_password.send_keys(cls.testuser_password)
        cls.browser.find_element_by_class_name("submit").click()

    @classmethod
    def tearDown(cls):
        cls.browser.quit()
        super().tearDown(cls)


class StpTemplateTest(SeleniumLoggedInTestCase):
    def test_index_template_click_on_certain_link(self):
        self.browser.get(self.live_server_url)
        # self.browser.implicitly_wait(10)
        self.browser.find_element_by_id('stp_detail_1').click()
        current_url = self.browser.current_url
        self.assertEqual(self.live_server_url + "/detail/1", current_url)


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
        self.assertTemplateUsed(response, "stp/campaign_list.html")
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
        self.assertTemplateUsed(response, "stp/campaign_detail.html")
        self.assertContains(response, c.name)
        item_set = Item.objects.filter(campaign=c)
        for item in item_set:
            self.assertContains(response, item.name)


class StpBasketItemFormTest(StpLoggedInTestCase):
    def setUp(self):
        self.item = Item.objects.get(pk=1)
        self.user = User.objects.get(username=self.testuser_username)

    def test_valid_data(self):
        form = BasketItemForm({'nos': "1"})
        self.assertTrue(form.is_valid())
        saved_basket_item = form.save()
        self.assertEqual(saved_basket_item.nos, 1)
        self.assertEqual(saved_basket_item.user, self.user)
        self.assertEqual(saved_basket_item.item, self.item)


class StpDetailTemplateTest(SeleniumLoggedInTestCase):
    # detail template には、id = form_item_#(pk(item)) をもつ form がitemごとに存在する。
    # submit ボタンを押すと、index にリダイレクトされる。
    # 適切なkeyを含んだpostが飛ぶことのテストはできていない。
    def test_detail_template_has_forms_for_every_items(self):
        self.browser.get(self.live_server_url + "/detail/1")
        item_set = Item.objects.filter(campaign=Campaign.objects.get(pk=1))
        for item in item_set:
            form = self.browser.find_element_by_id('id_form-' + str(item.pk - 1) + '-nos')
            form.send_keys('1')
        self.browser.find_element_by_id('submit').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/")


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
