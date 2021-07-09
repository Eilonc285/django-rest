from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Business


class TestSetUp(APITestCase):
    def setUp(self):
        Business(title='Mcdonalds', sub_title='Burger place', street='Sokolov', number=34, city='Beersheba',
                 grade=7.9).save()
        Business(title='Pizza Hut', sub_title='Pizza place', street='Hevron', number=18, city='Beersheba',
                 grade=8.2).save()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
