import datetime
import json
import re

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from user_chat.forms import SendMessageForm
from user_chat.models import Message, PrivateChat
from user_chat.serializers import MessageSerializer

User = get_user_model()


'''Web socket consumer for getting chat 
messages from users and send to other users'''
class MessageConsumer(AsyncJsonWebsocketConsumer):
    '''When connecting to the chat room'''
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    '''When disconnecting from the chat room'''
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        # Async accidents exceptions
        try:
            # if delete mode
            mode = content.pop('mode')
            chat_id = content.get('chat_id')
            if mode == 'delete':
                await self.delete_message(content.get('message_id'))
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        'type': 'send_message',
                        'data': {
                            'mode': 'delete',
                            'message_id': content.get('message_id'),
                            'last_message': await self.get_last_message(chat_id),
                        },
                    }
                )
            # if edit mode
            elif mode == 'edit':
                message_id = content.get('message_id')
                message = await self.update_message(content)
                message_html = render_to_string(
                    'current_user_message.html',
                    {'message': message.get('message'),
                     'chat': message.get('chat')}
                )
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        'type': 'send_message',
                        'data': {
                            'mode': 'edit',
                            'message_id': message_id,
                            'message_html': message_html,
                            'last_message': await self.get_last_message(chat_id),
                        },
                    }
                )
            # if create mode
            elif mode == 'send':
                message = await self.save_message(content)
                message_html = render_to_string(
                    'current_user_message.html',
                    {'message': message.get('message'),
                     'chat': message.get('chat')}
                )
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        'type': 'send_message',
                        'data': {
                            'mode': 'send',
                            'message_html': message_html,
                            'last_message': await self.get_last_message(chat_id),
                        }
                    }
                )
        except ZeroDivisionError:
            pass
        # except Exception:
        #     print("WebSocket consumer error")

    '''When editing the existing message'''
    @database_sync_to_async
    def update_message(self, data):
        data.pop('csrfmiddlewaretoken')
        message_id = data.pop('message_id')
        chat = get_object_or_404(
            PrivateChat,
            chat_id = data.pop('chat_id'),
        )
        Message.objects.filter(
            message_id=message_id
        ).update(
            **data,
            update_time=datetime.datetime.now()
        )
        return {
            'chat': chat,
            'message': Message.objects.get(message_id=message_id)
        }

    '''When deleting the existing message'''
    @database_sync_to_async
    def delete_message(self, message_id):
        Message.objects.get(message_id=message_id).delete()

    '''When saving a new message'''
    @database_sync_to_async
    def save_message(self, data):
        user_id = data.pop('user_id')
        chat_id = data.pop('chat_id')
        user = get_object_or_404(
            User,
            user_id=user_id
        )
        chat = get_object_or_404(
            PrivateChat,
            chat_id=chat_id
        )
        data.pop('csrfmiddlewaretoken')
        form = SendMessageForm()
        form.cleaned_data = {}
        form.cleaned_data.update(data)
        form.cleaned_data['message_id'] = \
            f'{chat_id}_{user_id}_' \
            f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
        form.save(user=user, chat=chat)
        return {'chat': chat,
                'message': get_object_or_404(
                    Message,
                    message_id=form.cleaned_data['message_id']
                )}

    '''Sending message back to all clients'''
    async def send_message(self, event):
        await self.send_json(content=event.get('data'))

    @database_sync_to_async
    def get_last_message(self, chat_id):
        last_message = MessageSerializer(
            PrivateChat.objects.get(
                chat_id=chat_id
            ).messages.last()
        ).data
        last_message['last_time'] = last_message.get('update_time') if \
            last_message.get('publish_time') != last_message.get('update_time') else \
            last_message.get('update_time')
        print(last_message.get('last_time'))
        last_time = re.match(
            r'^(?P<date>[\w-]+)T(?P<time>[\w:]+)\.',
            last_message.get('last_time')
        )
        last_message['last_time'] = f"" \
            f"{''.join(list(map(lambda x: x+'-', last_time['date'].split('-')[::-1])))[:-1]} {last_time['time']}"
        return last_message
