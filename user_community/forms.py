from django import forms
from django.forms import ModelForm
from user_community.models import Community
from user_community.utils import validate_community_name


'''Form of creation new community'''
class CommunityCreateForm(ModelForm):
    class Meta:
        model = Community
        fields = [
            'name',
            'is_public',
            'staff_list',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'is_public': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'staff_list': forms.SelectMultiple(
                attrs={'class': 'form-select'}
            )
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        validate_community_name(name)
        return name

    def __init__(self, *args, **kwargs):
        super(CommunityCreateForm, self).__init__(*args, **kwargs)
        self.fields['staff_list'].required = False


'''Form of editing the existing community'''
class CommunityEditForm(ModelForm):
    staff_edit = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'form-input'
        }),
        required=False,
    )
    class Meta:
        model = Community
        fields = [
            'name',
            'is_public',
            'preview_picture',
            'website',
            'vk',
            'instagram',
            'facebook',
            'twitter',
            'about',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'is_public': forms.Select(
                attrs={'class': 'form-input'}
            ),
            'preview_picture': forms.FileInput(
                attrs={'class': 'form-input'}
            ),
            'website': forms.URLInput(
                attrs={'class': 'form-input'}
            ),
            'vk': forms.URLInput(
                attrs={'class': 'form-input'}
            ),
            'instagram': forms.URLInput(
                attrs={'class': 'form-input'}
            ),
            'facebook': forms.URLInput(
                attrs={'class': 'form-input'}
            ),
            'twitter': forms.URLInput(
                attrs={'class': 'form-input'}
            ),
            'about': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
        }
