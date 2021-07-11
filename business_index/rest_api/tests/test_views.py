from .test_setup import TestSetUp
from django.urls import reverse
from unittest.mock import patch
from .. import models, views


class TestBusinessView(TestSetUp):
    def test_GET_all_businesses(self):
        response = self.client.get(reverse('rest_api:get_all'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Mcdonalds')
        self.assertContains(response, 'Pizza Hut')

    def test_GET_specific_business(self):
        response = self.client.get(reverse('rest_api:get_one', args=['0', 'Mcdonalds']))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Mcdonalds')
        self.assertContains(response, 'Burger place')


class TestWebScraperView(TestSetUp):
    def test_POST_for_existing_business(self):
        def mocked_scraper(data):
            return {'title': 'BBB', 'sub_title': 'Burger chain', 'grade': 7.7, 'street': 'ragger',
                    'number': 22, 'city': 'Beersheba'}

        views.get_first_business_info = mocked_scraper
        request = self.factory.post(reverse('rest_api:web_scraper'), data={'title': 'BBB', 'info': 'Burger'})
        request.data = {'title': 'BBB', 'info': 'Burger'}
        _view = views.WebScraperView()
        response = _view.post(request)
        self.assertEquals(response.status_code, 200)
        b = models.Business.objects.get(title='BBB')
        self.assertIsNotNone(b)

    def test_POST_for_non_existing_business(self):
        def mocked_scraper(data):
            return None

        views.get_first_business_info = mocked_scraper
        request = self.factory.post(reverse('rest_api:web_scraper'), data={'title': 'BBB', 'info': 'Burger'})
        request.data = {'title': 'BBB', 'info': 'Burger'}
        _view = views.WebScraperView()
        response = _view.post(request)
        self.assertEquals(response.status_code, 404)
        b = models.Business.objects.filter(title='BBB')
        self.assertEquals(len(b), 0)
