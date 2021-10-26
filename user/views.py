from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, FormView
from user.forms import UserRegisterForm, UserAuthenticationForm, UserMainDataEditForm, \
    UserBasicPersonalDataEditForm, UserContactDataEditForm, UserInterestsEditForm, \
    UserEducationAndSpecializationEditForm, UserDataVisibilityEditForm
from user.utils import UserViewMixin, get_user_state, UserEditMixin
from user_note.forms import NoteAddForm
from user_note.models import Note


User = get_user_model()


'''
View of user page, where user can
check and change his/her personal data,
add content and configure this page.
'''
class UserPageView(LoginRequiredMixin, UserViewMixin, TemplateView, FormView):
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
        context['notes'] = user.notes.all() | user.reposts.all()
        context['user'] = user
        context['authorised_user'] = self.request.user
        context['authorised_user_state'] = get_user_state(
            context['user'],
            context['authorised_user'],
        )
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
    extra_context = {'title': 'Sign In'}

    def get_success_url(self):
        return reverse_lazy('note_list')


'''
View of registration (sign up) page,
where user creates an account.
'''
class UserRegisterView(UserViewMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('note_list')
    extra_context = {'title': 'Sign Up'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('note_list')


class UserSettingsView(LoginRequiredMixin, UserViewMixin, TemplateView):
    template_name = 'user_settings.html'
    extra_context = {'title': 'Settings'}


class UserPasswordChangeView(UserEditMixin):
    extra_context = {'title': 'Password Change'}
    form_class = SetPasswordForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(UserPasswordChangeView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs


class UserMainDataEditView(UserEditMixin):
    form_class = UserMainDataEditForm
    extra_context = {'title': 'Main Data'}


class UserBasicPersonalDataEditView(UserEditMixin):
    form_class = UserBasicPersonalDataEditForm
    extra_context = {'title': 'Basic Data'}


class UserContactDataEditView(UserEditMixin):
    form_class = UserContactDataEditForm
    extra_context = {'title': 'Contact Data'}


class UserInterestsEditView(UserEditMixin):
    form_class = UserInterestsEditForm
    extra_context = {'title': 'Interests'}


class UserEducationAndSpecializationEditView(UserEditMixin):
    form_class = UserEducationAndSpecializationEditForm
    extra_context = {'title': 'Education and Specialization'}


class UserDataVisibilityEditView(UserEditMixin):
    form_class = UserDataVisibilityEditForm
    extra_context = {'title': 'Data Visibility'}
