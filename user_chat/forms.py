from django import forms
from django.core.exceptions import ValidationError
from multiupload import fields
from .models import Message, GroupChat
from user_note.utils import attach_media


'''Get user friend list for select widget'''
def get_user_friends(instance):
    friends = instance.user.friends.all()
    choices = []
    for friend in friends:
        choices.append((friend, f'{friend.first_name} {friends.last_name}'))
    return choices


'''SendMessageForm allowing to send messages to other users in chats'''
class SendMessageForm(forms.ModelForm):
    images = fields.MultiImageField(
        min_num=0,
        max_num=10,
        attrs={
            'class': 'image-button',
        },
    )
    videos = fields.MultiMediaField(
        min_num=0,
        max_num=10,
        media_type='video',
        attrs={
            'class': 'video-button',
        },
    )
    audios = fields.MultiMediaField(
        min_num=0,
        max_num=10,
        media_type='audio',
        attrs={
            'class': 'audio-button',
        },
    )
    files = fields.MultiFileField(
        min_num=0,
        max_num=10,
        attrs={
            'class': 'file-button',
        },
    )

    def __init__(self, *args, **kwargs):
        super(SendMessageForm, self).__init__(*args, **kwargs)
        self.fields['text'].required = False

    class Meta:
        model = Message
        fields = [
            'text',
        ]
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 1,
                    'class': 'form-input',
                    'placeholder': 'Message text here',
                }
            )
        }

    def save(self, commit=True, user=None, chat=None):
        media = {
            'images': self.cleaned_data.pop('images', []),
            'videos': self.cleaned_data.pop('videos', []),
            'audios': self.cleaned_data.pop('audios', []),
            'files': self.cleaned_data.pop('files', []),
        }
        self.cleaned_data['sender'] = user
        message = Message(**self.cleaned_data)
        message = attach_media(media, 'user', user, message)
        message.save()
        chat.messages.add(message)
        return message


'''
CreateGroupChatForm allowing to create 
group chats and invite your friends into them
'''
class CreateGroupChatForm(forms.ModelForm):
    members = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select',
            },
        ),
        choices=get_user_friends,
    )
    staff = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select',
            },
        ),
        choices=get_user_friends,
    )

    class Meta:
        model = GroupChat
        fields = [
            'name',
            'picture',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'from-input',
                },
            ),
            'picture': forms.ClearableFileInput(
                attrs={
                    'class': 'from-input',
                },
            ),
        }

    def clean(self):
        members = self.cleaned_data.get('members')
        staff = self.cleaned_data.get('staff')
        for user in staff:
            if user not in members:
                raise ValidationError(
                    'Staff users must be chat members'
                )
        return self.cleaned_data

    def save(self, commit=True, user=None):
        self.cleaned_data['members'].append(user)
        self.cleaned_data['staff'].append(user)
        group_chat = GroupChat(**self.cleaned_data)
        group_chat.save()
        for member in self.cleaned_data['members']:
            member.group_chats.add(group_chat)
        user.group_chats.add(group_chat)
        return group_chat
