from .test_setup import TestSetUp
from django.urls import reverse
from unittest.mock import patch
from ..models import Business


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
    def test_POST_for_business(self):
        with patch('rest_api.easy_web_scraper.get_first_business_info') as mocked_scrape:
            mocked_scrape.return_value = {'title': 'BBB', 'sub_title': 'Burger chain', 'grade': 7.7, 'street': 'ragger',
                                          'number': 22, 'city': 'Beersheba'}
            response = self.client.post(reverse('rest_api:web_scraper'), data={'title': 'BBB', 'info': 'Burger'})
            self.assertEquals(response.status_code, 200)
            b = Business.objects.get(title='BBB')
            self.assertIsNotNone(b)
