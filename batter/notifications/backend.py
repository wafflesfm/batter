from django.utils.translation import ugettext

from notification import backends

from . import models

class ModelBackend(backends.BaseBackend):
    spam_sensitivity = 1

    def deliver(self, recipient, notice_type, extra_context):
        context = self.default_context()
        context.update({
            "recipient": recipient,
            "notice": ugettext(notice_type.display)
        })
        context.update(extra_context)

        messages = self.get_formatted_message({
            "short.txt",
            "full.txt",
            "short.html",
            "full.html"
        }, notice_type.label, context)

        notification = models.Notification()
        notification.recipient = recipient

        notification.title = messages["short.html"]
        notification.body = messages["full.html"]
        notification.title_text = messages["short.txt"]
        notification.body_text = messages["full.txt"]
        
        notification.save()