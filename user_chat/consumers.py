import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from user_chat.forms import SendMessageForm
from user_chat.models import Message, PrivateChat


User = get_user_model()


'''Web socket for getting chat messages'''
class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        # if delete mode
        try:
            if text_data_json.pop('delete', None):
                await self.delete_message(text_data_json.get('message_id'))
                await self.send(text_data=f'delete{text_data_json.get("message_id")}')
            # if edit mode
            elif text_data_json.pop('edit', None):
                message = await self.update_message(text_data_json)
                message_html = render_to_string(
                    'current_user_message.html',
                    {'message': message.get('message'),
                     'chat': message.get('chat')}
                )
                await self.send(text_data='edit'+message_html)
            # if create mode
            else:
                message = await self.save_message(text_data_json)
                await self.add_message(
                    message.get('chat'),
                    message.get('message')
                )
        except:
            pass

    @database_sync_to_async
    def update_message(self, data):
        csrf = data.pop('csrfmiddlewaretoken')
        message_id = data.pop('message_id')
        chat = get_object_or_404(
            PrivateChat,
            chat_id = data.pop('chat_id'),
        )
        Message.objects.filter(
            message_id=message_id
        ).update(**data)
        return {
            'chat': chat,
            'message': Message.objects.get(message_id=message_id)
        }

    @database_sync_to_async
    def delete_message(self, message_id):
        Message.objects.get(message_id=message_id).delete()

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
        csrf = data.pop('csrfmiddlewaretoken')
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

    async def add_message(self, chat, message):
        message_html = render_to_string(
            'current_user_message.html',
            {'message': message,
            'chat': chat}
        )
        await self.send(text_data=message_html)
