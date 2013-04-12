from django.utils.translation import ugettext

from notification import backends

from . import models

class ModelBackend(backends.BaseBackend):
    def deliver(self, recipient, notice_type, extra_context):
        context = self.default_context()
        context.update({
            "recipient": recipient,
            "notice": ugettext(notice_type.display)
        })
        context.update(extra_context)

        messages = self.get_formatted_message({
            "short.txt",
            "full.txt"
        }, notice_type.label, context)

        title, body = messages["short.txt"], messages["full.txt"]

        notification = models.Notification.new(recipient, title, body)
        notification.save()