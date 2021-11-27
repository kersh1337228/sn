from rest_framework import serializers
from user_chat.models import Message


'''Chat message serializer for WebSocket processing'''
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'