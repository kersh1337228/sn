from django import forms
from django.contrib.auth import get_user_model
from user_note.models import Note
from multiupload import fields
from user_note.utils import note_attach_media


User = get_user_model()


'''
Form to add notes, placed on user page,
feed page and community page.
'''
class NoteAddForm(forms.ModelForm):
    images = fields.MultiImageField(min_num=0, max_num=20)
    videos = fields.MultiMediaField(min_num=0, max_num=20, media_type='video')
    audios = fields.MultiMediaField(min_num=0, max_num=20, media_type='audio')
    files = fields.MultiFileField(min_num=0, max_num=20)

    class Meta:
        model = Note
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'cols': 60,
                'rows': 3,
                'class': 'form-input',
                'placeholder': 'Note text here',
            })
        }

    '''
    Redefined save method, allowing to 
    upload multiple media files per one time.
    '''
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
