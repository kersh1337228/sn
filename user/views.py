from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, FormView
from user.forms import UserRegisterForm, UserAuthenticationForm
from user.utils import UserViewMixin
from user_note.forms import NoteAddForm
from user_note.models import Note


User = get_user_model()


'''
View of user page, where user can
check and change his/her personal data,
add content and configure this page.
'''
class UserPageView(UserViewMixin, TemplateView, FormView):
    model = User
    context_object_name = 'user'
    template_name = 'user_page.html'
    slug_url_kwarg = 'user_id'
    form_class = NoteAddForm

    def get_success_url(self):
        return reverse_lazy(
            'user_page',
            kwargs={
                'user_id': self.kwargs.get('user_id')
            }
        )

    def get_user_profile(self):
        return get_object_or_404(User, user_id=self.kwargs.get('user_id'))

    def get_context_data(self, **kwargs):
        user = self.get_user_profile()
        context = super().get_context_data(**kwargs)
        context['title'] = f'{user.first_name} {user.last_name}'
        context['notes'] = Note.objects.filter(
            Q(user=user) |
            Q(community__in=user.community_subscribes.all())
        )
        context['user'] = self.get_user_profile()
        return context

    def form_valid(self, form):
        form.save(user=self.get_user_profile())
        return super(UserPageView, self).form_valid(form)


'''
View of authentication (sign in) page,
where user logs in.
'''
class UserAuthenticationView(UserViewMixin, LoginView):
    form_class = UserAuthenticationForm
    template_name = 'sign_in.html'

    def get_success_url(self):
        return reverse_lazy('note_list')

    def get_user_context(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign in'
        return context


'''
View of registration (sign up) page,
where user creates an account.
'''
class UserRegisterView(UserViewMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('note_list')

    def get_user_context(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign up'
        return context
