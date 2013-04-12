from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=512)

    sent_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField()

    @classmethod
    def new(cls, recipient, title, body):
        """ Create a new Notification """
        notification = cls()
        notification.recipient = recipient
        notification.title = title
        notification.body = body
        return notification

    def seen(self):
        """ Mark a Notification as having been seen """
        self.seen = True
        self.seen_at = now()
        return self

    @property
    def as_object(self):
        """ Prepare a Notification for display, via e.g. JSON """
        return {
            "title": self.title,
            "body": self.body,
            "seen": self.seen,
            "sent_at": self.sent_at
        }