'''
User models is a site core.
Every other app is connected with this one.
Here are the models of user app,
allowing to register (sign up),
authorize (sign in), edit and delete
users database entries.
'''


from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from additional_databases.add_dbs import get_cities, get_countries, \
    get_languages, get_universities


'''
Customised user-manager, replacing built-in
Django user-manager and extending it's functional.
'''
class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        user = self.model(**kwargs)
        user.set_password(kwargs['password'])
        user.save(using=self._db)
        return user

    def create_staffuser(self, **kwargs):
        user = self.model(**kwargs)
        user.staff = True
        user.set_password(kwargs['password'])
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.model(**kwargs)
        user.staff = True
        user.admin = True
        user.set_password(kwargs['password'])
        user.save(using=self._db)
        return user


'''
Customised user-model, replacing built-in
Django user-model and extending it's functional.
'''
class User(AbstractBaseUser):
    '''User authentication data'''
    email = models.EmailField(
        verbose_name='Email-address',
        max_length=255,
        null=False,
        blank=False,
        unique=True,
    )
    phone_number = PhoneNumberField(
        verbose_name='Phone-number',
        null=False,
        blank=False,
        unique=True,
    )
    user_id = models.SlugField(
        verbose_name='User ID',
        max_length=255,
        null=False,
        blank=True,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=255,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=255,
        null=False,
        blank=False,
    )
    gender = models.CharField(
        verbose_name='Gender',
        null=False,
        blank=False,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
    )
    birthdate = models.DateField(
        verbose_name='Birthdate',
        null=False,
        blank=False,
    )
    # PasswordField is automatically created by parent class
    personal_information = models.OneToOneField(
        'UserData',
        auto_created=True,
        on_delete=models.CASCADE,
    )
    is_public = models.BooleanField(
        verbose_name='Private or Public account',
        null=False,
        blank=False,
        default=False,
        choices=[
            (True, 'Public'),
            (False, 'Private'),
        ]
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'gender', 'birthdate']

    def get_absolute_url(self):
        return self.user_id

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.user_id

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['last_name', 'first_name']


'''
User data model, storing connected databases,
divided into certain categories, depending on
a kind of user information.
'''
class UserData(models.Model):
    basic_data = models.OneToOneField(
        'UserBasicData',
        auto_created=True,
        on_delete=models.CASCADE,
    )
    contact_info = models.OneToOneField(
        'UserContactData',
        auto_created=True,
        on_delete=models.CASCADE,
    )
    interests = models.OneToOneField(
        'UserInterests',
        auto_created=True,
        on_delete=models.CASCADE,
    )
    education = models.OneToOneField(
        'UserEducation',
        auto_created=True,
        on_delete=models.CASCADE,
    )
    work = models.OneToOneField(
        'UserWork',
        auto_created=True,
        on_delete=models.CASCADE,
    )
    fields_visibility = models.OneToOneField(
        'UserDataVisibility',
        auto_created=True,
        on_delete=models.CASCADE,
    )


'''
Basic user data which allows 
to identify the person.
'''
class UserBasicData(models.Model):
    current_city = models.CharField(
        verbose_name='Current city',
        null=True,
        blank=True,
        default=None,
        choices=get_cities(),
    )
    languages = models.CharField(
        verbose_name='Languages',
        null=True,
        blank=True,
        default=None,
        choices=get_languages(),
    )
    company = models.CharField(
        verbose_name='Company',
        null=True,
        blank=True,
        default=None,
    )
    relationship = models.NullBooleanField(
        verbose_name='Relationship',
        null=True,
        blank=True,
        default=None,
        choices=[
            (None, 'None selected'),
            (False, 'Single'),
            (True, 'Have a pair'),
        ],
    )


'''
User contact data, allowing to contact person
or to find his page on another platforms.
'''
class UserContactData(models.Model):
    country = models.CharField(
        verbose_name='Country',
        null=True,
        blank=True,
        default=None,
        choices=get_countries(),
    )
    city = models.CharField(
        verbose_name='Country',
        null=True,
        blank=True,
        default=None,
        choices=[city for city in get_cities() if city[0]['country_id'] == country],
    )
    alternative_phone_number = PhoneNumberField(
        verbose_name='Alternative phone-number',
        null=True,
        blank=True,
        default=None,
        unique=True,
    )
    website = models.URLField(
        verbose_name='Website',
        null=True,
        blank=True,
        default=None,
    )
    vk = models.URLField(
        verbose_name='Website',
        null=True,
        blank=True,
        default=None,
    )
    instagram = models.URLField(
        verbose_name='Website',
        null=True,
        blank=True,
        default=None,
    )
    facebook = models.URLField(
        verbose_name='Website',
        null=True,
        blank=True,
        default=None,
    )
    twitter = models.URLField(
        verbose_name='Website',
        null=True,
        blank=True,
        default=None,
    )


'''
Personal user interests, including information
about his favorite films, TV series, games, books and etc.
Also includes brief about me section.
'''
class UserInterests(models.Model):
    activities = models.TextField(
        verbose_name='Activities',
        max_length=8191,
        null=True,
        blank=True,
        default=None,
    )
    interests = models.TextField(
        verbose_name='Interests',
        max_length=8191,
        null=True,
        blank=True,
        default=None,
    )
    favorite_music = models.TextField(
        verbose_name='Favorite music',
        max_length=8191,
        null=True,
        blank=True,
        default=None,
    )
    favorite_movies = models.TextField(
        verbose_name='Favorite movies and TV series',
        max_length=8191,
        null=True,
        blank=True,
        default=None,
    )
    favorite_books = models.TextField(
        verbose_name='Favorite books',
        max_length=8191,
        null=True,
        blank=True,
        default=None,
    )
    favorite_games = models.TextField(
        verbose_name='Favorite games',
        max_length=8191,
        null=True,
        blank=True,
        default=None,
    )
    about_me = models.TextField(
        verbose_name='About me',
        max_length=32767,
        null=True,
        blank=True,
        default=None,
    )


'''Information about user's secondary and higher education'''
class UserEducation(models.Model):
    education_secondary = models.CharField(
        verbose_name='Secondary education',
        null=True,
        blank=True,
        default=None,
    )
    education_higher = models.CharField(
        verbose_name='Higher education',
        null=True,
        blank=True,
        default=None,
        choices=get_universities(),
    )


'''Information about user's current career position'''
class UserWork(models.Model):
    company = models.CharField(
        verbose_name='Company',
        max_length=255,
        null=True,
        blank=True,
        default=None,
    )
    specialization = models.CharField(
        verbose_name='Specialization',
        max_length=255,
        null=True,
        blank=True,
        default=None,
    )


'''Says whether to show some of user's personal data or not'''
class UserDataVisibility(models.Model):
    email_visible = models.BooleanField(
        verbose_name='Show email',
        null=False,
        blank=True,
        default=False,
        choices=[
            (True, 'Show my email'),
            (False, 'Do not show my email')
        ],
    )
    phone_number_visible = models.BooleanField(
        verbose_name='Show phone number',
        null=False,
        blank=True,
        default=False,
        choices=[
            (True, 'Show my phone number'),
            (False, 'Do not show my phone number')
        ],
    )
    birthdate_visible = models.BooleanField(
        verbose_name='Show birthdate',
        null=False,
        blank=True,
        default=False,
        choices=[
            (True, 'Show my birthdate'),
            (False, 'Do not show my birthdate')
        ],
    )
