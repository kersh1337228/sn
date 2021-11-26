import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from user_chat.forms import SendMessageForm
from user_chat.models import Message, PrivateChat


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

    # async def receive_json(self, content, **kwargs):
    #     text_data_json = json.loads(text_data)
    #     # Async accidents exceptions
    #     try:
    #         # if delete mode
    #         if text_data_json.pop('delete', None):
    #             await self.delete_message(text_data_json.get('message_id'))
    #             await self.channel_layer.group_send(
    #                 self.chat_group_name,
    #                 {
    #                     'type': 'send_message',
    #                     'data': f'delete{text_data_json.get("message_id")}',
    #                 }
    #             )
    #         # if edit mode
    #         elif text_data_json.pop('edit', None):
    #             message_id = text_data_json.get('message_id')
    #             message = await self.update_message(text_data_json)
    #             message_html = render_to_string(
    #                 'current_user_message.html',
    #                 {'message': message.get('message'),
    #                  'chat': message.get('chat')}
    #             )
    #             await self.channel_layer.group_send(
    #                 self.chat_group_name,
    #                 {
    #                     'type': 'send_message',
    #                     'data': 'edit' + message_id + message_html,
    #                 }
    #             )
    #         # if create mode
    #         else:
    #             message = await self.save_message(text_data_json)
    #             message_html = render_to_string(
    #                 'current_user_message.html',
    #                 {'message': message.get('message'),
    #                  'chat': message.get('chat')}
    #             )
    #             await self.channel_layer.group_send(
    #                 self.chat_group_name,
    #                 {
    #                     'type': 'send_message',
    #                     'data': message_html,
    #                 }
    #             )
    #     except:
    #         pass

    '''When getting the user message from client'''
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        # Async accidents exceptions
        try:
            # if delete mode
            if text_data_json.pop('delete', None):
                await self.delete_message(text_data_json.get('message_id'))
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        'type': 'send_message',
                        'data': f'delete{text_data_json.get("message_id")}',
                    }
                )
            # if edit mode
            elif text_data_json.pop('edit', None):
                message_id = text_data_json.get('message_id')
                message = await self.update_message(text_data_json)
                message_html = render_to_string(
                    'current_user_message.html',
                    {'message': message.get('message'),
                     'chat': message.get('chat')}
                )
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        'type': 'send_message',
                        'data': 'edit' + message_id + message_html,
                    }
                )
            # if create mode
            else:
                message = await self.save_message(text_data_json)
                message_html = render_to_string(
                    'current_user_message.html',
                    {'message': message.get('message'),
                     'chat': message.get('chat')}
                )
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        'type': 'send_message',
                        'data': message_html,
                    }
                )
        except:
            pass

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
        ).update(**data)
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
        # await self.send(text_data=event.get('data'))
        await self.send({'some': 'test', 'data': event.get('data')})
