from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Notification


class NotificationTests(TestCase):
    def setUp(self):
        self.samantha = User.objects.create_user(
            'samantha',
            'samantha@example.com',
            'soliloquy'
        )
        self.joe = User.objects.create_user(
            'joe',
            'joe@example.com',
            'antiphony'
        )
        self.samantha_mail, _ = Notification.objects.get_or_create(
            recipient=self.samantha,
            title='You\'ve got mail!',
            body='joe sent you a message',
            title_text='You\'ve got mail!',
            body_text='joe sent you a message'
        )

    def test_model_mark_seen(self):
        self.assertEquals(self.samantha_mail.seen, False)
        self.assertIsNone(self.samantha_mail.seen_at)

        self.samantha_mail.mark_seen().save()

        self.assertEquals(self.samantha_mail.seen, True)
        self.assertIsNotNone(self.samantha_mail.seen_at)

    def test_manager_by_user(self):
        results = Notification.objects.by_user(self.samantha)

        self.assertIn(self.samantha_mail, results)
        self.assertEqual(len(results), 1)

    def test_manager_by_other_user(self):
        results = Notification.objects.by_user(self.joe)

        self.assertEqual(len(results), 0)

    def test_queryset_unseen(self):
        results = Notification.objects.by_user(self.samantha).unseen()

        self.assertIn(self.samantha_mail, results)

        self.samantha_mail.mark_seen().save()

        results = Notification.objects.by_user(self.samantha).unseen()

        self.assertNotIn(self.samantha_mail, results)

    def test_queryset_mark_seen(self):
        self.assertEquals(self.samantha_mail.seen, False)

        results = Notification.objects.by_user(self.samantha).unseen()
        results.mark_seen()

        self.samantha_mail = Notification.objects.get(
            pk=self.samantha_mail.pk
        )

        self.assertEquals(self.samantha_mail.seen, True)

    def test_model_as_dict(self):
        obj = self.samantha_mail.as_dict()
        self.assertIn("text", obj)
        self.assertIn("html", obj)
        self.assertIn("seen", obj)
        self.assertEquals(obj['seen'], False)
        self.assertIsNotNone(obj['sent_at'])
        self.assertEquals(obj['text']['title'], "You've got mail!")
        self.assertEquals(obj['text']['body'], "joe sent you a message")
        self.assertEquals(obj['html']['title'], "You've got mail!")
        self.assertEquals(obj['html']['body'], "joe sent you a message")
