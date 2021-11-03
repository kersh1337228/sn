from django import forms
from django.contrib.auth import get_user_model
from user_note.models import Note, Comment, PostMixin
from multiupload import fields
from user_note.utils import note_attach_media


User = get_user_model()


class PostFormMixin(forms.ModelForm):
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
                'rows': 3,
                'class': 'form-input',
                'placeholder': 'Text here',
            })
        }

    def __init__(self, *args, **kwargs):
        super(PostFormMixin, self).__init__(*args, **kwargs)
        self.fields['text'].required = True


'''
Form to add notes, placed on user page,
feed page and community page.
'''
class NoteAddForm(PostFormMixin):
    '''
    Redefined save method, allowing to 
    upload multiple media files per one time.
    '''
    def __init__(self, *args, **kwargs):
        try:
            print("some")
            super(NoteAddForm, self).__init__(*args, **kwargs)
        except TypeError:
            super(NoteAddForm, self).__init__()
        self.cleaned_data = {}
        self.text = self.cleaned_data['text'] = kwargs.get('text')
        self.images = self.cleaned_data['images'] = kwargs.get('images')
        self.videos = self.cleaned_data['videos'] = kwargs.get('videos')
        self.audios = self.cleaned_data['audios'] = kwargs.get('audios')
        self.files = self.cleaned_data['files'] = kwargs.get('files')
        self.cleaned_data['note_id'] = kwargs.get('note_id')

    def save(self, commit=True, user=None, community=None):
        images = self.cleaned_data.pop('images')
        videos = self.cleaned_data.pop('videos')
        audios = self.cleaned_data.pop('audios')
        files = self.cleaned_data.pop('files')
        if user:
            self.cleaned_data['user'] = user
            note = Note(**self.cleaned_data)
            note = note_attach_media(images, 'image', 'user', user, note)
            note = note_attach_media(videos, 'video', 'user', user, note)
            note = note_attach_media(audios, 'audio', 'user', user, note)
            note = note_attach_media(files, 'file', 'user', user, note)
            note.save()
            user.notes.add(note)
        else:
            self.cleaned_data['community'] = community
            note = Note(**self.cleaned_data)
            note = note_attach_media(images, 'image', 'community', community, note)
            note = note_attach_media(videos, 'video', 'community', community, note)
            note = note_attach_media(audios, 'audio', 'community', community, note)
            note = note_attach_media(files, 'file', 'community', community, note)
            note.save()
            community.notes.add(note)
        return note


'''Form to add comments under content'''
class CommentAddForm(PostFormMixin):
    def __init__(self, *args, **kwargs):
        super(CommentAddForm, self).__init__()
        self.cleaned_data = {}
        self.text = self.cleaned_data['text'] = kwargs.get('text')
        self.images = self.cleaned_data['images'] = kwargs.get('images')
        self.videos = self.cleaned_data['videos'] = kwargs.get('videos')
        self.audios = self.cleaned_data['audios'] = kwargs.get('audios')
        self.files = self.cleaned_data['files'] = kwargs.get('files')
        self.cleaned_data['comment_id'] = kwargs.get('comment_id')

    def save(self, commit=True, user=None, community=None, note=None):
        images = self.cleaned_data.pop('images')
        videos = self.cleaned_data.pop('videos')
        audios = self.cleaned_data.pop('audios')
        files = self.cleaned_data.pop('files')
        self.cleaned_data['note_commented'] = note
        if user:
            self.cleaned_data['user'] = user
            comment = Comment(**self.cleaned_data)
            comment = note_attach_media(images, 'image', 'user', user, comment)
            comment = note_attach_media(videos, 'video', 'user', user, comment)
            comment = note_attach_media(audios, 'audio', 'user', user, comment)
            comment = note_attach_media(files, 'file', 'user', user, comment)
        else:
            self.cleaned_data['community'] = community
            comment = Note(**self.cleaned_data)
            comment = note_attach_media(images, 'image', 'community', community, comment)
            comment = note_attach_media(videos, 'video', 'community', community, comment)
            comment = note_attach_media(audios, 'audio', 'community', community, comment)
            comment = note_attach_media(files, 'file', 'community', community, comment)
        comment.save()
        note.comments.add(comment)
        return note