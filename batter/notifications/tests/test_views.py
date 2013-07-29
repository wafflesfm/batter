import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Notification


class BaseNotificationTests(TestCase):
    def setUp(self):
        self.samantha = User.objects.create_user(
            'samantha',
            'samantha@example.com',
            'soliloquy'
        )
        self.samantha_mail, _ = Notification.objects.get_or_create(
            recipient=self.samantha,
            title='You\'ve got mail!',
            body='joe sent you a message',
            title_text='You\'ve got mail!',
            body_text='joe sent you a message'
        )

    def generate_bunk(self, num):
        bunk = []
        for i in range(num):
            n, _ = Notification.objects.get_or_create(
                recipient=self.samantha,
                title='You\'ve got mail! ' + str(i),
                body='joe sent you a message',
                title_text='You\'ve got mail!' + str(i),
                body_text='joe sent you a message'
            )
            bunk.append(n)
        return bunk

    def login(self):
        self.client.login(username='samantha', password='soliloquy')


class NotificationAPITests(BaseNotificationTests):
    def fetch_list_response(self):
        url = reverse('notifications_list')
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        return response

    def fetch_list(self):
        self.login()
        response = self.fetch_list_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        return data

    def test_list_authentication(self):
        response = self.fetch_list_response()
        self.assertEquals(response.status_code, 302)
        self.assertIn('signin', response['Location'])

    def test_list_pagination(self):
        self.generate_bunk(60)
        data = self.fetch_list()
        self.assertIn('total', data)
        self.assertEquals(data['total'], 61)
        self.assertIn('pages', data)
        self.assertIn('count', data['pages'])
        self.assertEquals(len(data['results']), 10)
        self.assertEquals(data['pages']['count'], 7)

    def test_list_single(self):
        data = self.fetch_list()
        self.assertEquals(len(data['results']), 1)
        result = data['results'][0]
        self.assertEquals(result['seen'], False)


class NotificationHTMLTests(BaseNotificationTests):
    def fetch_list_response(self, data={}):
        url = reverse('notifications_list')
        response = self.client.get(url, data=data)
        return response

    def fetch_list(self, data={}):
        self.login()
        response = self.fetch_list_response(data)
        self.assertEquals(response.status_code, 200)
        return response

    def test_list_authentication(self):
        response = self.fetch_list_response()
        self.assertEquals(response.status_code, 302)
        self.assertIn('signin', response['Location'])

    def test_list_pagination(self):
        self.generate_bunk(60)
        response = self.fetch_list()
        self.assertEquals(len(response.context['object_list']), 20)
        self.assertIsNotNone(response.context['paginator'])
        self.assertEquals(response.context['is_paginated'], True)

    def test_list_pagination_page_2(self):
        self.generate_bunk(60)
        response = self.fetch_list(data={'page': 2})
        self.assertEquals(len(response.context['object_list']), 20)
