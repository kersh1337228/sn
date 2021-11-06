import datetime
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import model_to_dict
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView
from user.forms import UserRegisterForm, UserAuthenticationForm, UserMainDataEditForm, \
    UserBasicPersonalDataEditForm, UserContactDataEditForm, UserInterestsEditForm, \
    UserEducationAndSpecializationEditForm, UserDataVisibilityEditForm
from user.utils import UserViewMixin, get_user_state, UserEditMixin
from user_note.forms import PostAddForm
from user_note.models import Note, Like, Comment, Reply
from django.http import HttpResponseRedirect


User = get_user_model()


'''The decorator to check if current user is not active'''
def functionally_based_view_decorator(view):
    def actual_decorator(request, *args, **kwargs):
        if request.user.is_active:
            return view(request, *args, **kwargs)
        else:
            context = {
                'title': 'Error',
                'error_message': 'No such user',
            }
            return redirect(
                'error.html',
                context=context
            )
    return actual_decorator


class UserPageMixin(LoginRequiredMixin, UserViewMixin, TemplateView, FormView):
    model = User
    context_object_name = 'user'
    slug_url_kwarg = 'user_id'

    def get_success_url(self):
        return reverse_lazy(
            'user_page',
            kwargs={
                'user_id': self.kwargs.get('user_id')
            }
        )

    def get_user_profile(self):
        return get_object_or_404(
            User,
            user_id=self.kwargs.get('user_id')
        )

    def get_context_data(self, **kwargs):
        user = self.get_user_profile()
        context = super().get_context_data(**kwargs)
        context['title'] = f'{user.first_name} {user.last_name}'
        context['notes'] = user.notes.all() | user.reposts.all()
        context['user'] = user
        context['authorised_user_state'] = get_user_state(
            context['user'],
            self.request.user,
        )
        return context


'''
View of user page, where user can
check and change his/her personal data,
add content and configure this page.
'''
class UserPageView(UserPageMixin):
    form_class = PostAddForm
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if 'note_btn' in self.request.POST:
            form.save(
                owner=self.request.user,
                owner_type='user',
                object_model=Note,
                type='note',
                parent=self.request.user
            )
        elif 'comment_btn' in self.request.POST:
            note_id = [key for key in self.request.POST if '_note_' in key][0]
            form.save(
                owner=self.request.user,
                owner_type='user',
                object_model=Comment,
                type='comment',
                parent=get_object_or_404(Note, note_id=note_id)
            )
        elif 'reply_btn' in self.request.POST:
            comment_id = [key for key in self.request.POST if '_comment_' in key][0]
            form.save(
                owner=self.request.user,
                owner_type='user',
                object_model=Reply,
                type='reply',
                parent=get_object_or_404(Comment, comment_id=comment_id)
            )
        return super(UserPageView, self).form_valid(form)


class UserPageEditPostView(UserPageView):
    def get_template_names(self):
        if self.kwargs.get('reply_id'):
            return 'user_page_edit_reply.html'
        elif self.kwargs.get('comment_id'):
            return 'user_page_edit_comment.html'
        elif self.kwargs.get('note_id'):
            return 'user_page_edit_note.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('reply_id'):
            context['current_reply_id'] = self.kwargs.get('reply_id')
        if self.kwargs.get('comment_id'):
            context['current_comment_id'] = self.kwargs.get('comment_id')
        if self.kwargs.get('note_id'):
            context['current_note_id'] = self.kwargs.get('note_id')
        return context

    def get_initial(self):
        if self.kwargs.get('reply_id'):
            self.type = 'reply'
            self.type_model = Reply
        elif self.kwargs.get('comment_id'):
            self.type = 'comment'
            self.type_model = Comment
        elif self.kwargs.get('note_id'):
            self.type = 'note'
            self.type_model = Note
        initial = super().get_initial()
        initial.update(
            **model_to_dict(
                self.type_model.objects.get(
                    **{f'{self.type}_id': self.kwargs.get(f'{self.type}_id')}
                )
            )
        )
        return initial

    def form_valid(self, form):
        self.type_model.objects.filter(
            **{f'{self.type}_id': self.kwargs.get(f'{self.type}_id')}
        ).update(
            text=form.cleaned_data.get('text'),
            update_time=datetime.datetime.now()
        )
        return HttpResponseRedirect(self.get_success_url())


@login_required
@functionally_based_view_decorator
def delete_view(request, **kwargs):
    if kwargs.get('reply_id'):
        Reply.objects.get(
            reply_id=kwargs.get('reply_id')
        ).delete()
    elif kwargs.get('comment_id'):
        Comment.objects.get(
            comment_id=kwargs.get('comment_id')
        ).delete()
    elif kwargs.get('note_id'):
        Note.objects.get(
            note_id=kwargs.get('note_id')
        ).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required
@functionally_based_view_decorator
def like_view(request, **kwargs):
    def like(type, model, id, action):
        object = get_object_or_404(
            model,
            **{f'{type}_id': id}
        )
        if action == 'like':
            like = Like(
                user=request.user,
                **{type: object}
            )
            like.save()
            object.likes.add(like)
            object.liked_by.add(request.user)
        elif action == 'dislike':
            like = get_object_or_404(
                Like,
                user=request.user,
                **{type: object}
            )
            like.delete()
            object.liked_by.remove(request.user)
    if kwargs.get('reply_id'):
        like(
            'reply',
            Reply,
            kwargs.get('reply_id'),
            kwargs.get('action'),
        )
    elif kwargs.get('comment_id'):
        like(
            'comment',
            Comment,
            kwargs.get('comment_id'),
            kwargs.get('action'),
        )
    elif kwargs.get('note_id'):
        like(
            'note',
            Note,
            kwargs.get('note_id'),
            kwargs.get('action'),
        )
    return redirect(request.META['HTTP_REFERER'])


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


'''View of changing user profile picture'''
class UserProfilePictureEditView(LoginRequiredMixin, UserViewMixin, TemplateView):
    pass


'''The list of all user account settings'''
class UserSettingsView(LoginRequiredMixin, UserViewMixin, TemplateView):
    template_name = 'user_settings.html'
    extra_context = {'title': 'Settings'}


'''Change the password'''
class UserPasswordChangeView(UserEditMixin):
    extra_context = {'title': 'Password Change'}
    form_class = SetPasswordForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(UserPasswordChangeView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs


'''Main data which is listed during registration'''
class UserMainDataEditView(UserEditMixin):
    form_class = UserMainDataEditForm
    extra_context = {'title': 'Main Data'}


'''Personal data'''
class UserBasicPersonalDataEditView(UserEditMixin):
    form_class = UserBasicPersonalDataEditForm
    extra_context = {'title': 'Basic Data'}


'''User contacts'''
class UserContactDataEditView(UserEditMixin):
    form_class = UserContactDataEditForm
    extra_context = {'title': 'Contact Data'}


'''User interests'''
class UserInterestsEditView(UserEditMixin):
    form_class = UserInterestsEditForm
    extra_context = {'title': 'Interests'}


'''User education and specialization'''
class UserEducationAndSpecializationEditView(UserEditMixin):
    form_class = UserEducationAndSpecializationEditForm
    extra_context = {'title': 'Education and Specialization'}


'''User data visibility for other users'''
class UserDataVisibilityEditView(UserEditMixin):
    form_class = UserDataVisibilityEditForm
    extra_context = {'title': 'Data Visibility'}
