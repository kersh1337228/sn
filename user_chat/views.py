import datetime
from itertools import chain
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
from user_community.forms import SearchForm
from .forms import CreateGroupChatForm, SendMessageForm
from .models import PrivateChat, GroupChat, Message
from .serializers import MessageSerializer


User = get_user_model()


'''Chat mixing for PrivateChat and GroupChat'''
class ChatMixin(LoginRequiredMixin, DetailView, FormView):
    context_object_name = 'chat'
    template_name = 'private_chat.html'
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


'''ChatListView allowing to see user's chat list'''
class ChatListView(LoginRequiredMixin, ListView, FormView):
    model = PrivateChat
    template_name = 'chat_list.html'
    form_class = SearchForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = kwargs
        context['title'] = 'Chat list'
        context['private_chats'] = self.request.user.private_chats.all()
        context['group_chats'] = self.request.user.group_chats.all()
        context['chats'] = list(chain(
            self.request.user.private_chats.all(),
            self.request.user.group_chats.all()
        ))
        return context

    def get_initial(self):
        initial = super().get_initial()
        if self.kwargs.get('search'):
            initial.update(
                search_text=self.kwargs.get('search')
            )
        return initial

    def form_valid(self, form):
        return redirect(
            'community_search_list',
            search=form.cleaned_data.get('search_text')
        )


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


'''View allowing to get the message according to it's id'''
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


@login_required
@functionally_based_view_decorator
def get_chats_view(request):
    filter = request.GET.get('filter')
    chats_html = ''; chat_list = []
    if filter == 'all':
        chat_list = list(chain(
            request.user.private_chats.all(),
            request.user.group_chats.all()
        ))
    elif filter == 'private':
        chat_list = request.user.private_chats.all()
    elif filter == 'group':
        chat_list = request.user.group_chats.all()
    if chat_list:
        for chat in chat_list:
            chats_html += render_to_string(
                'chat_min.html',
                {
                    'chat': chat,
                    'request': request,
                    'private_chats': request.user.private_chats.all(),
                    'group_chats': request.user.group_chats.all(),
                }
            )
    else:
        chats_html = 'No chats yet'
    return JsonResponse({'chats': chats_html}, status=200)
