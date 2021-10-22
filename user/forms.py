from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from phonenumber_field.formfields import validate_international_phonenumber
from user.utils import validate_name


User = get_user_model()


'''Form of creation new account (sign up)'''
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
            'phone_number' : forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-input'}
            ),
            'password1': forms.PasswordInput(
                attrs={'class': 'form-input'}
            ),
            'password2': forms.PasswordInput(
                attrs={'class': 'form-input'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'gender': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'birthdate': forms.SelectDateWidget(
                attrs={'class': 'form-select'},
                years= [str(year) for year in range(1940, 2004)]
            ),
            'is_public': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }

    '''Phone number validation'''
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        validate_international_phonenumber(phone_number)
        return phone_number

    '''First name validation'''
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        validate_name(first_name, 'first name')
        return first_name

    '''Last name validation'''
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        validate_name(last_name, 'last name')
        return last_name


'''
Redefined basic Django UserAuthenticationForm,
so it can either use phone_number or email as username.
'''
class AuthenticationForm(forms.Form):
    '''
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    '''
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'autofocus': True
        }),
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password'
        }),
    )

    error_messages = {
        'invalid_login': "Please enter a correct %(username)s and password. "
                         "Note that both fields may be case-sensitive.",
        'inactive': 'This account is inactive.',
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        self.fields['username'].max_length = self.fields['username'].widget.attrs['maxlength'] = 255
        if self.fields['username'].label is None:
            self.fields['username'].label = 'Phone or email'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Checking if email address or phone number is entered
        if '@' in username:
            validate_email(username)
            username = User.objects.get(email=username).phone_number
        else:
            validate_international_phonenumber(username)

        # Trying to authenticate
        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    # Checking that the profile is not blocked or deleted
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    # Getting current user object
    def get_user(self):
        return self.user_cache

    # Login validation inner form error
    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': 'Phone or email'},
        )


'''Form of user authentication (sign in)'''
class UserAuthenticationForm(AuthenticationForm):
    '''
    Defines whether an email address or
    a phone number is entered and
    validates these fields.
    '''
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)


'''Form of editing main user account data'''
class UserMainDataEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'phone_number',
            'email',
            'first_name',
            'last_name',
            'gender',
            'birthdate',
            'is_public',
        ]
        widgets = {
            'phone_number': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-input'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'gender': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'birthdate': forms.SelectDateWidget(
                attrs={'class': 'form-select'},
                years=[str(year) for year in range(1940, 2004)]
            ),
            'is_public': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }


'''Form of editing basic personal data'''
class UserBasicPersonalDataEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'current_city',
            'languages',
            'company',
            'relationship',
        ]
        widgets = {
            'current_city': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'languages': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'company': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'relationship': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }


'''Form of editing user contact data'''
class UserContactDataEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'country',
            'city',
            'alternative_phone_number',
            'website',
            'vk',
            'instagram',
            'facebook',
            'twitter'
        ]
        widgets = {
            'country': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'city': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'alternative_phone_number': forms.TextInput(
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
        }


'''Form of editing user interests data'''
class UserInterestsEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'activities',
            'interests',
            'favorite_music',
            'favorite_movies',
            'favorite_books',
            'favorite_games',
            'about_me',
        ]
        widgets = {
            'activities': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'interests': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'favorite_music': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'favorite_movies': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'favorite_books': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'favorite_games': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'about_me': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
        }


'''Form of editing user education data'''
class UserEducationAndSpecializationEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'education_secondary',
            'education_higher',
            'specialization',
        ]
        widgets = {
            'education_secondary': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'education_higher': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'specialization': forms.TextInput(
                attrs={'class': 'form-input'}
            )
        }


'''Form of editing user data visibility settings'''
class UserDataVisibilityEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email_visible',
            'phone_number_visible',
            'birthdate_visible',
        ]
        widgets = {
            'email_visible': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'phone_number_visible': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'birthdate_visible': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }
