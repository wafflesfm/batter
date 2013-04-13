from . import models


def notifications(request):
    """
    Context processor for notifications

    This is required because I don't want to override Django's
    RelatedManager, so it's easier to attack this problem in reverse.
    """
    user = request.user
    if user.is_authenticated():
        notifications = models.Notification.objects.by_user(user).unseen()
        return {
            'unseen_notifications': notifications
        }
    else:
        return {}
