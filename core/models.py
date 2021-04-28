from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils import timezone
from django.utils.text import slugify
from django_countries.fields import CountryField
from PIL import Image
from django.core.files.storage import default_storage
from io import BytesIO


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    objects = CustomUserManager()
    MALE = 'M'
    FEMALE = 'F'
    GENDER_OPTIONS = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer_not_to_say', 'Prefer not to say')
    ]

    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=100, unique=True,
                                help_text='Required.')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    birthdate = models.DateField(default=timezone.now)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=GENDER_OPTIONS,
        blank=False,
        default='')
    country = CountryField(default='US')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.email)

    # def get_friends(self):
    #     friends = Friend.objects.filter(User=self.User)
    #     return friends

    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.username
            self.slug = slugify(value, allow_unicode=True)
        super().save()


# class CustomLink(models.Model):
#     title = models.CharField(max_length=100, help_text="The title of your link")
#     link = models.URLField(blank=True, max_length=200)
#     owner = models.OneToOneField(User, on_delete=models.CASCADE, editable=False, default=None)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    profile_image = models.ImageField(upload_to="images/profile_images",default='catcomputer.png')
    background_image = models.ImageField(upload_to="images/profile_images",default='catcomputer.png')

    # Social media links
    facebook_link = models.URLField(blank=True, max_length=200)
    instagram_link = models.URLField(blank=True, max_length=200)
    twitter_link = models.URLField(blank=True, max_length=200)
    youtube_link = models.URLField(blank=True, max_length=200)
    patreon_link = models.URLField(blank=True, max_length=200)
    twitch_link = models.URLField(blank=True, max_length=200)

    # custom_link = models.ForeignKey(CustomLink, on_delete=models.CASCADE, blank=True, null=True)

    about_me = models.TextField(default='Add something about yourself here!')

    # Public link. AKA the link that the user shares with the world
    public_link = models.URLField(blank=True, max_length=200)

    def __str__(self):
        return str(self.user.username)
    
    # def save(self, *args, **kwargs):
    #     memfile = BytesIO()

    #     img = Image.open(self.image)
    #     if img.height > 1000 or img.width > 1000:
    #         output_size = (1000, 1000)
    #         img.thumbnail(output_size, Image.ANTIALIAS)
    #         img.save(memfile, 'JPEG', quality=95)
    #         default_storage.save(self.image.name, memfile)
    #         memfile.close()
    #         img.close()

