import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, CreateView, ListView, DetailView
from user.views import functionally_based_view_decorator
from .forms import CreateGroupChatForm, SendMessageForm
from .models import PrivateChat, GroupChat, Message
from .utils import ExtraContentMixin


User = get_user_model()


class ChatMixin(LoginRequiredMixin, DetailView, FormView):
    context_object_name = 'chat'
    template_name = 'private_chat.html'
    slug_url_kwarg = 'chat_id'
    form_class = SendMessageForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().chat_id
        return context

    def get_success_url(self):
        return redirect(self.request.META['HTTP_REFERER'])

    def form_valid(self, form):
        if self.request.method == 'POST' and self.request.is_ajax():
            form.cleaned_data['message_id'] = \
                f'{self.get_object().chat_id}_' \
                f'{self.request.user.user_id}_' \
                f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
            form.save(user=self.request.user, chat=self.get_object())
            message = render_to_string(
                'current_user_message.html',
                {'message': get_object_or_404(
                    Message,
                    message_id=form.cleaned_data['message_id']
                ), 'chat': get_object_or_404(
                    PrivateChat,
                    chat_id=self.kwargs.get('chat_id')
                )})
            return JsonResponse({'message': message}, status=200)
        return super(ChatMixin, self).form_valid(form)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)


'''ChatListView allowing to see user's chat list'''
class ChatListView(LoginRequiredMixin, ExtraContentMixin, ListView):
    model = PrivateChat
    template_name = 'chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return PrivateChat.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chat list'
        context['private_chats'] = self.request.user.private_chats.all()
        context['group_chats'] = self.request.user.group_chats.all()
        return context

    def get_private_chats(self):
        return self.request.user.private_chats.all()

    def get_group_chats(self):
        return self.request.user.group_chats.all()



'''
PrivateChatView allowing to use 
chats to communicate between two users
'''
class PrivateChatView(ChatMixin):
    model = PrivateChat

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            return JsonResponse(
                {'messages':
                    list(self.get_object().messages.all().values())
                },
                status=200
            )
        return super(PrivateChatView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(PrivateChat, chat_id=self.kwargs.get('chat_id'))


'''
PrivateChatEditMessageView allowing 
to edit message you have already sent
'''
class PrivateChatEditMessageView(PrivateChatView):
    def get(self, request, *args, **kwargs):
        super(PrivateChatEditMessageView, self).get(request, *args, **kwargs)
        return JsonResponse(
            {'initial': self.get_initial(),
             'form': render_to_string(
                'form.html',
                 {'form': self.get_form_class(),
                  'type': 'message',
                  'message': get_object_or_404(
                      Message,
                      message_id=self.kwargs.get('message_id')
                  )},
             request=request,
             )},
            status=200)

    def get_initial(self):
        initial = super().get_initial()
        initial.update(
            **model_to_dict(
                self.get_object().messages.get(message_id=self.kwargs.get('message_id'))
            )
        )
        return initial

    def form_valid(self, form):
        if self.request.method == 'POST' and self.request.is_ajax():
            message_id = [key for key in self.request.POST if '_' in key][0]
            Message.objects.filter(
                message_id=message_id
            ).update(
                text=form.cleaned_data.get('text'),
                update_time=datetime.datetime.now()
            )
            message = render_to_string(
                'current_user_message.html',
                {'message': get_object_or_404(
                    Message,
                    message_id=message_id
                ), 'chat': get_object_or_404(
                    PrivateChat,
                    chat_id=self.kwargs.get('chat_id')
                )})
            return JsonResponse(
                {'message': message},
                status=200,
            )
        return super(ChatMixin, self).form_valid(form)


'''
private_chat_delete_message_view allowing
to delete the message you have already sent
'''
@csrf_exempt
@login_required(login_url='signin')
@functionally_based_view_decorator
def private_chat_delete_message_view(request, chat_id, message_id):
    if request.method == 'DELETE' and request.is_ajax():
        get_object_or_404(Message, message_id=message_id).delete()
        return JsonResponse({}, status=200)
    # return redirect(request.META['HTTP_REFERER'])
    return HttpResponse('get')


'''
GroupChatView allowing to use 
chats to communicate between multiple users
'''
class GroupChatView(ChatMixin):
    model = GroupChat

    def get_object(self, queryset=None):
        return get_object_or_404(GroupChat, chat_id=self.kwargs.get('chat_id'))

'''
create_private_chat_view allowing to create 
private chat between current user and another
'''
@login_required
def create_private_chat_view(request, member_id):
    user = request.user
    if user.is_active:
        member = get_object_or_404(User, user_id=member_id)
        try:
            private_chat = PrivateChat.objects.get(
                Q(member_1=user, member_2=member) |
                Q(member_2=user, member_1=member)
            )
        except:
            private_chat = PrivateChat(
                member_1=user,
                member_2=member,
            )
            private_chat.save()
            user.private_chats.add(private_chat)
            member.private_chats.add(private_chat)
        return redirect(
            'private_chat',
            chat_id=private_chat.chat_id
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
CreateGroupChatView allowing to create 
group chat and invite your friends there
'''
class CreateGroupChatView(LoginRequiredMixin, FormView, CreateView):
    model = GroupChat
    form_class = CreateGroupChatForm
    template_name = 'create_group_chat.html'

    def get_success_url(self):
        return reverse_lazy(
            'group_chat',
            kwargs={
                'chat_id': self.kwargs.get('chat_id')
            }
        )

    def form_valid(self, form):
        form.save(user=self.request.user)
        return redirect(
            'group_chat',
            chat_id=GroupChat.objects.get(name=form.cleaned_data.get('name')).chat_id
        )
