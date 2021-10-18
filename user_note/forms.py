from django import forms
from django.contrib.auth import get_user_model
from user_note.models import Note, NoteImage, NoteVideo,\
    NoteAudio, NoteFile
from multiupload import fields


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
        else:
            self.cleaned_data['community'] = community
        if self.cleaned_data.get('user'):
            for image in images:
                img = NoteImage(
                    image=image,
                    user=self.cleaned_data.get('user'),
                    note=self.instance
                )
                img.save()
            for video in videos:
                vid = NoteVideo(
                    video=video,
                    user=self.cleaned_data.get('user'),
                    note=self.instance
                )
                vid.save()
            for audio in audios:
                aud = NoteAudio(
                    audio=audio,
                    user=self.cleaned_data.get('user'),
                    note=self.instance
                )
                aud.save()
            for file in files:
                fil = NoteFile(
                    file=file,
                    user=self.cleaned_data.get('user'),
                    note=self.instance
                )
                fil.save()
        else:
            for image in images:
                img = NoteImage(
                    image=image, community=self.cleaned_data.get('community'), note=self.instance
                )
                img.save()
            for video in videos:
                vid = NoteVideo(
                    video=video, community=self.cleaned_data.get('community'), note=self.instance
                )
                vid.save()
            for audio in audios:
                aud = NoteAudio(
                    audio=audio, community=self.cleaned_data.get('community'), note=self.instance
                )
                aud.save()
            for file in files:
                fil = NoteFile(
                    file=file, community=self.cleaned_data.get('community'), note=self.instance
                )
                fil.save()
        note = Note(**self.cleaned_data)
        note.save()
        return note
