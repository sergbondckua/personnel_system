from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Головна сторінка кадрової системи.
    """

    template_name = "dashboard/index.html"
