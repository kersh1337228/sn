import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView
from .forms import SendMessageForm


class ExtraContentMixin():
    def get_user_context(self, **kwargs):
        context = kwargs
        return context
