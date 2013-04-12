from django.db import models
from django.db.models.query import QuerySet
from django.conf import settings
from django.utils.timezone import now


class NotificationQuerySet(QuerySet):
    def mark_seen(self):
        return self.update(seen=True, seen_at=now())

    def unseen(self):
        return self.filter(seen=False)


class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model)

    def by_user(self, user):
        return self.get_queryset().filter(recipient=user)


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='notifications'
    )

    title = models.TextField(blank=False, null=False)
    body = models.TextField(blank=False, null=False)
    title_text = models.TextField(blank=True, null=False)
    body_text = models.TextField(blank=True, null=False)

    seen = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    seen_at = models.DateTimeField(null=True)

    objects = NotificationManager()

    def mark_seen(self):
        """ Mark a Notification as having been seen """
        self.seen = True
        self.seen_at = now()
        return self

    @property
    def as_object(self):
        """ Prepare a Notification for display, via e.g. JSON """
        return {
            "text": {
                "title": self.title_text,
                "body": self.body_text,
            },
            "html": {
                "title": self.title,
                "body": self.body,
            },
            "seen": self.seen,
            "sent_at": self.sent_at,
        }
