from django import forms
from django.contrib.auth import get_user_model
from user_note.models import PostMixin
from multiupload import fields
from user_note.utils import attach_media


User = get_user_model()


class PostAddForm(forms.ModelForm):
    images = fields.MultiImageField(min_num=0, max_num=20)
    videos = fields.MultiMediaField(min_num=0, max_num=20, media_type='video')
    audios = fields.MultiMediaField(min_num=0, max_num=20, media_type='audio')
    files = fields.MultiFileField(min_num=0, max_num=20)

    class Meta:
        model = PostMixin
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'cols': 60,
                'rows': 1,
                'class': 'form-input',
                'placeholder': 'Text here',
            })
        }

    def __init__(self, *args, **kwargs):
        super(PostAddForm, self).__init__(*args, **kwargs)
        self.fields['text'].required = True

    def save(self, commit=True, *args, **kwargs):
        media = {
            'images': self.cleaned_data.pop('images'),
            'videos': self.cleaned_data.pop('videos'),
            'audios': self.cleaned_data.pop('audios'),
            'files': self.cleaned_data.pop('files'),
        }
        self.cleaned_data[kwargs.get("owner_type")] = kwargs.get('owner')
        object = kwargs.get('object_model')(**self.cleaned_data)
        object = attach_media(media, kwargs.get('owner_type'), kwargs.get('owner'), object)
        object.save()
        if kwargs.get('type') == 'note':
            kwargs.get('parent').notes.add(object)
        elif kwargs.get('type') == 'comment':
            kwargs.get('parent').comments.add(object)
        elif kwargs.get('type') == 'reply':
            kwargs.get('parent').replies.add(object)
        return object
