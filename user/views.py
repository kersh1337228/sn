from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from user.forms import UserRegisterForm, UserAuthenticationForm
from user.utils import UserViewMixin


User = get_user_model()


'''
View of user page, where user can
check and change his/her personal data,
add content and configure this page.
'''
class UserPageView(UserViewMixin, TemplateView):
    model = User
    template_name = 'user_page.html'
    context_object_name = 'user'
    slug_url_kwarg = 'user_id'

    def get_user_profile(self):
        return get_object_or_404(User, user_id=self.kwargs.get('user_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.get_user_profile().first_name} {self.get_user_profile().last_name}'
        return context


'''
View of authentication (sign in) page,
where user logs in.
'''
class UserAuthenticationView(UserViewMixin, LoginView):
    form_class = UserAuthenticationForm
    template_name = 'sign_in.html'

    def get_success_url(self):
        return reverse_lazy('user_note')

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
    success_url = reverse_lazy('user_note')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('user_note')

    def get_user_context(self, **kwargs):
        context = dict(
            list(super().get_context_data(**kwargs).items()) +
            list(self.get_context_data(title='Sign up').items())
        )
        return context
