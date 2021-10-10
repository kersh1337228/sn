from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email
from phonenumber_field.formfields import PhoneNumberField, validate_international_phonenumber


User = get_user_model()


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'phone_number',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'gender',
            'birthdate',
            'is_public',
        ]
        widgets = {
            'phone_number' : PhoneNumberField(attrs={'class': 'form-input'}),
            'email': forms.EmailField(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'gender': forms.ChoiceField(attrs={'class': 'form-input'}),
            'birthdate': forms.DateField(attrs={'class': 'form-input'}),
            'is_public': forms.ChoiceField(attrs={'class': 'form-input'}),
        }


class UserAuthenticationForm(AuthenticationForm):
    phone_or_email = forms.CharField(
        label='Phone number or email address',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    '''
    Defines whether an email address or
    a phone number is entered and
    validates these fields.
    '''
    def clean_phone_or_email(self):
        cleaned_data = self.cleaned_data
        phone_or_email = cleaned_data.get('phone_or_email')
        if '@' in phone_or_email:
            validate_email(phone_or_email)
        else:
            validate_international_phonenumber(phone_or_email)
        return cleaned_data

