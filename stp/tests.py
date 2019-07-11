from django.test import TestCase
from django.urls import reverse

from stp.models import BasketItem, Item


class StpViewTest(TestCase):
    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, "Hello world!")


class StpModelTest(TestCase):
    # BasketItem に要素を何も追加しなかったら、カウントは０
    def test_basket_item_is_empty(self):
        saved_basket_items = BasketItem.objects.all()
        self.assertEqual(saved_basket_items.count(), 0)

    # BasketItem に要素を一つ追加したら、カウントは１
    def test_basket_item_is_not_empty(self):
        basket_item = BasketItem()
        basket_item.save()
        saved_basket_items = BasketItem.objects.all()
        self.assertEqual(saved_basket_items.count(), 1)

    # BasketItem は item: Item(models.Model) を要素に持つ
    def test_basket_item_has_item(self):
        basket_item = BasketItem()
        basket_item.save()
        first_basket_item = BasketItem.objects.first()
        self.assertIsInstance(first_basket_item.item, Item)
