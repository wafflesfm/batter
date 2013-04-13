from django.views.generic.list import ListView

from braces.views import LoginRequiredMixin, JSONResponseMixin, \
    AjaxResponseMixin

from . import models


class NotificationList(
    LoginRequiredMixin,
    JSONResponseMixin,
    AjaxResponseMixin,
    ListView
):
    http_method_names = ['get']  # get only
    allow_empty = True
    template_name = "notifications/list.html"
    ajax_show_on_page = 10
    content_type = 'text/html'

    def get_queryset(self):
        qs = models.Notification.objects.by_user(self.request.user)
        qs.mark_seen()
        return qs

    def get_ajax(self, request):
        self.object_list = self.get_queryset()
        self.content_type = 'application/json'

        paginator, page, object_list, more_pages = self.paginate_queryset(
            self.object_list,
            self.ajax_show_on_page
        )

        next_p = page.next_page_number() if page.has_next() else None
        prev_p = page.previous_page_number() if page.has_previous() else None
        return self.render_json_response({
            'total': paginator.count,
            'pages': {
                'count': paginator.num_pages,
                'next': next_p,
                'previous': prev_p,
            },
            'results': list(object_list),  # force iterable to be a list
        })
