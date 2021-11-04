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
from user_note.forms import NoteAddForm, CommentAddForm, PostFormMixin, ReplyAddForm
from user_note.models import Note, Like, Comment, Reply


User = get_user_model()


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


'''
View of user page, where user can
check and change his/her personal data,
add content and configure this page.
'''
class UserPageView(UserPageMixin):
    form_class = PostFormMixin
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note_add_form'] = NoteAddForm
        context['comment_add_form'] = CommentAddForm
        return context

    def form_valid(self, form):
        if 'note_btn' in self.request.POST:
            note_add_view(self.request, form)
        elif 'comment_btn' in self.request.POST:
            note_id = [key for key in self.request.POST if '_note_' in key][0]
            comment_add_view(self.request, form, note_id)
        elif 'reply_btn' in self.request.POST:
            comment_id = [key for key in self.request.POST if '_comment_' in key][0]
            reply_add_view(self.request, form, comment_id)
        return super(UserPageView, self).form_valid(form)


@login_required
def note_add_view(request, form):
    user = request.user
    if user.is_active:
        if request.method == 'POST':
            form.cleaned_data['note_id'] = \
                f'{user.user_id}_note_' \
                f'{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
            note_add_form = NoteAddForm(**form.cleaned_data)
            note_add_form.save(user=user)
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect(
            'error.html',
            context=context
        )


@login_required
def comment_add_view(request, form, note_id):
    user = request.user
    if user.is_active:
        note = get_object_or_404(Note, note_id=note_id)
        if request.method == 'POST':
            form.cleaned_data['comment_id'] = \
                f'{note_id}_comment_' \
                f'{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
            comment_add_form = CommentAddForm(**form.cleaned_data)
            comment_add_form.save(user=user, note=note)
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect(
            'error.html',
            context=context
        )


@login_required
def reply_add_view(request, form, comment_id):
    user = request.user
    if user.is_active:
        comment = get_object_or_404(Comment, comment_id=comment_id)
        if request.method == 'POST':
            form.cleaned_data['reply_id'] = \
                f'{comment_id}_reply_' \
                f'{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
            reply_add_form = ReplyAddForm(**form.cleaned_data)
            reply_add_form.save(user=user, comment=comment)
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect(
            'error.html',
            context=context
        )


'''
UserPageEditNoteView allowing to 
edit the note you have already posted
'''
class UserPageEditNoteView(UserPageMixin):
    form_class = NoteAddForm
    template_name = 'user_page_edit_note.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_note_id'] = self.kwargs.get('note_id')
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial.update(
            **model_to_dict(
                Note.objects.get(
                    note_id=self.kwargs.get('note_id')
                )
            )
        )
        return initial

    def form_valid(self, form):
        Note.objects.filter(
            note_id=self.kwargs.get('note_id')
        ).update(
            text=form.cleaned_data.get('text'),
            update_time=datetime.datetime.now()
        )
        return super(UserPageEditNoteView, self).form_valid(form)


'''
user_page_delete_note_view allowing to 
delete the note you have already posted
'''
@login_required
def user_page_delete_note_view(request, user_id, note_id):
    user = get_object_or_404(User, user_id=user_id)
    if user.is_active:
        Note.objects.get(
            note_id=note_id
        ).delete()
        return redirect(
            'user_page',
            user_id=user.user_id
        )
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect(
            'error.html',
            context=context
        )


@login_required
def note_like_view(request, user_id, note_id, action):
    user = request.user
    if user.is_active:
        note = get_object_or_404(Note, note_id=note_id)
        if action == 'like':
            like = Like(
                user=user,
                note=note
            )
            like.save()
            note.likes.add(like)
            note.liked_by.add(user)
        elif action == 'dislike':
            like = get_object_or_404(
                Like,
                user=user,
                note=note,
            )
            like.delete()
            note.liked_by.remove(user)
        return redirect(
            'user_page',
            user_id=user.user_id
        )
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect(
            'error.html',
            context=context
        )


@login_required
def comment_like_view(request, user_id, note_id, comment_id, action):
    user = request.user
    if user.is_active:
        comment = get_object_or_404(Comment, comment_id=comment_id)
        if action == 'like':
            like = Like(
                user=user,
                comment=comment
            )
            like.save()
            comment.likes.add(like)
            comment.liked_by.add(user)
        elif action == 'dislike':
            like = get_object_or_404(
                Like,
                user=user,
                comment=comment,
            )
            like.delete()
            comment.liked_by.remove(user)
        return redirect(
            'user_page',
            user_id=user.user_id
        )
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect(
            'error.html',
            context=context
        )


class UserPageEditCommentView(UserPageMixin):
    form_class = CommentAddForm
    template_name = 'user_page_edit_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_note_id'] = self.kwargs.get('note_id')
        context['current_comment_id'] = self.kwargs.get('comment_id')
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial.update(
            **model_to_dict(
                Comment.objects.get(
                    comment_id=self.kwargs.get('comment_id')
                )
            )
        )
        return initial

    def form_valid(self, form):
        Comment.objects.filter(
            comment_id=self.kwargs.get('comment_id')
        ).update(
            text=form.cleaned_data.get('text'),
            update_time=datetime.datetime.now()
        )
        return super(UserPageEditCommentView, self).form_valid(form)


@login_required
def user_page_delete_comment_view(request, user_id, note_id, comment_id):
    user = get_object_or_404(User, user_id=user_id)
    if user.is_active:
        Comment.objects.get(
            comment_id=comment_id
        ).delete()
        return redirect(
            'user_page',
            user_id=user.user_id
        )
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect(
            'error.html',
            context=context
        )


@login_required
def reply_like_view(request, user_id, note_id, comment_id, reply_id, action):
    user = request.user
    if user.is_active:
        reply = get_object_or_404(Reply, reply_id=reply_id)
        if action == 'like':
            like = Like(
                user=user,
                reply=reply
            )
            like.save()
            reply.likes.add(like)
            reply.liked_by.add(user)
        elif action == 'dislike':
            like = get_object_or_404(
                Like,
                user=user,
                reply=reply,
            )
            like.delete()
            reply.liked_by.remove(user)
        return redirect(
            'user_page',
            user_id=user.user_id
        )
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect(
            'error.html',
            context=context
        )


class UserPageEditReplyView(UserPageMixin):
    form_class = ReplyAddForm
    template_name = 'user_page_edit_reply.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_note_id'] = self.kwargs.get('note_id')
        context['current_comment_id'] = self.kwargs.get('comment_id')
        context['current_reply_id'] = self.kwargs.get('reply_id')
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial.update(
            **model_to_dict(
                Reply.objects.get(
                    reply_id=self.kwargs.get('reply_id')
                )
            )
        )
        return initial

    def form_valid(self, form):
        Reply.objects.filter(
            reply_id=self.kwargs.get('reply_id')
        ).update(
            text=form.cleaned_data.get('text'),
            update_time=datetime.datetime.now()
        )
        return super(UserPageEditReplyView, self).form_valid(form)


@login_required
def user_page_delete_reply_view(request, user_id, note_id, comment_id, reply_id):
    user = get_object_or_404(User, user_id=user_id)
    if user.is_active:
        Reply.objects.get(
            reply_id=reply_id
        ).delete()
        return redirect(
            'user_page',
            user_id=user.user_id
        )
    else:
        context = {
            'title': 'Error',
            'error_message': 'No such user',
        }
        return redirect(
            'error.html',
            context=context
        )


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
