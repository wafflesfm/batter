import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Notification


class NotificationsContextProcessorTests(TestCase):
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

    def test_authenticated(self):
        self.client.login(username='samantha', password='soliloquy')
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertIn('unseen_notifications', response.context)

    def test_unauthenticated(self):
        response = self.client.get('/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('unseen_notifications', response.context)
