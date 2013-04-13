from django.test import TestCase
from django.contrib.auth.models import User

from notification.models import NoticeType

from ..backend import ModelBackend
from ..models import Notification

class StubbedModelBackend(ModelBackend):
    def get_formatted_messages(self, templates, label, context):
        return dict(zip(templates, ['message'] * len(templates)))

class ModelBackendTests(TestCase):
    def setUp(self):
        self.backend = StubbedModelBackend('stubmodel')
        self.samantha = User.objects.create_user(
            'samantha',
            'samantha@example.com',
            'soliloquy'
        )
        self.new_message, _ = NoticeType.objects.get_or_create(
            label='mail',
            display='New Private Message',
            description='Notification when you receive a private message',
            default=1
        )

    def test_deliver(self):
        self.backend.deliver(
            recipient=self.samantha,
            notice_type=self.new_message,
            extra_context={}
        )
        results = Notification.objects.by_user(self.samantha).unseen()
        self.assertEquals(len(results), 1)

        notification = results.get()
        self.assertEquals(notification.title, 'message')
        self.assertEquals(notification.body, 'message')
        self.assertEquals(notification.title_text, 'message')
        self.assertEquals(notification.body_text, 'message')