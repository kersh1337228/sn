from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView, DetailView

from user.views import functionally_based_view_decorator
from .forms import CreateGroupChatForm, SendMessageForm
from .models import PrivateChat, GroupChat, Message
from .serializers import MessageSerializer
from .utils import ChatMixin, ExtraContentMixin


User = get_user_model()


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

    def get_object(self, queryset=None):
        return get_object_or_404(PrivateChat, chat_id=self.kwargs.get('chat_id'))


'''
PrivateChatEditMessageView allowing 
to edit message you have already sent
'''
class PrivateChatEditMessageView(PrivateChatView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {'form': render_to_string(
                 'form.html',
                 {'form': self.get_form_class()(initial=self.get_initial()),
                  'type': 'message',
                  'message': get_object_or_404(
                      Message,
                      message_id=self.kwargs.get('message_id')
                  )},
                 request=request,
             )},
            status=200)

    def get_initial(self):
        serializer = MessageSerializer(
            self.get_object().messages.get(
                message_id=self.kwargs.get('message_id')
            )
        )
        return serializer.data


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
@functionally_based_view_decorator
def create_private_chat_view(request, member_id):
    member = get_object_or_404(User, user_id=member_id)
    try:
        private_chat = PrivateChat.objects.get(
            Q(member_1=request.user, member_2=member) |
            Q(member_2=request.user, member_1=member)
        )
    except:
        private_chat = PrivateChat(
            member_1=request.user,
            member_2=member,
        )
        private_chat.save()
        request.user.private_chats.add(private_chat)
        member.private_chats.add(private_chat)
    return redirect(
        'private_chat',
        chat_id=private_chat.chat_id
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


@login_required
@functionally_based_view_decorator
def get_message_view(request, chat_id, message_id):
    return JsonResponse(
        {'message': render_to_string(
            'current_user_message.html',
            {'message': get_object_or_404(Message, message_id=message_id),
             'chat': get_object_or_404(PrivateChat, chat_id=chat_id)}
        )},
        status=200
    )
