from django.views.generic.detail import DetailView
from django.utils import timezone

from Register.models import Register


class RegisterDetailView(DetailView):

    model = Register
    context_object_name = "register"
    template_name = "registered_detail.html"

    def get_context_data(self, **kwargs):
        context = super(RegisterDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context