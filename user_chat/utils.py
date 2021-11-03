import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView
from .forms import SendMessageForm


class ChatMixin(LoginRequiredMixin, DetailView, FormView):
    context_object_name = 'chat'
    template_name = 'chat.html'
    slug_url_kwarg = 'chat_id'
    form_class = SendMessageForm

    def get_user_context(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.chat_id
        return context

    def get_success_url(self):
        return reverse_lazy(
            'private_chat',
            kwargs={
                'chat_id': self.kwargs.get('chat_id'),
            },
        )

    def form_valid(self, form):
        form.cleaned_data['message_id'] = \
            f'{self.get_object().chat_id}_' \
            f'{self.request.user.user_id}_' \
            f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
        form.save(user=self.request.user, chat=self.get_object())
        return super(ChatMixin, self).form_valid(form)


class ExtraContentMixin():
    def get_user_context(self, **kwargs):
        context = kwargs
        return context
