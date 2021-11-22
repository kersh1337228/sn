from rest_framework import serializers
from user_chat.models import Message


'''Chat message serializer for WebSocket processing'''
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'images', 'videos', 'audios',
            'files', 'text'
        )