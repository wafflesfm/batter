from django.core.urlresolvers import resolve
from django.shortcuts import redirect
from django.views.generic.detail import DetailView


class EnforcingSlugDetailView(DetailView):
    """
    A DetailView that looks up by pk but enforces a valid slug in the url.
    """
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        current_url = resolve(request.path_info).url_name

        if self.get_object().slug != slug:
            return redirect(current_url,
                            pk=self.object.pk,
                            slug=self.object.slug,
                            permanent=True)

        return super(EnforcingSlugDetailView, self).dispatch(request,
                                                             *args,
                                                             **kwargs)
