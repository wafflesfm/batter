from django.test import TestCase
from django.contrib.auth.models import User


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'samantha',
            'samantha@example.com',
            'soliloquy'
        )
        self.client.login(username='samantha', password='soliloquy')
