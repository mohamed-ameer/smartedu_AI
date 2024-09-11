from django.db import models
from django.contrib.auth.models import User
import os
from django.db.models.signals import post_save
from PIL import Image
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

def user_directory_path_profile(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = 'user_{0}/{1}'.format(instance.user.id,filename)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)
        
    return profile_pic_name

def user_directory_path_banner(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    banner_pic_name = 'user_{0}/{1}'.format(instance.user.id,filename)
    full_path = os.path.join(settings.MEDIA_ROOT, banner_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return banner_pic_name

university = (
    ('Zagazig_University', 'Zagazig _University'),
    ('Cairo_University', 'Cairo_University'),
    ('Ain_Shams_University', 'Ain_Shams_University'),
)
user_types = (
    ('student', 'student'),
    ('teacher', 'teacher'),
)
major_types = (
    ('civil_engineering', 'civil_engineering'),
    ('chemical_engineering', 'chemical_engineering'),
    ('mechanical_engineering', 'mechanical_engineering'),
    ('electrical_engineering', 'electrical_engineering'),
    ('industrial_engineering', 'industrial_engineering'),
)
class Profile(models.Model):
    user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_directory_path_profile, blank=True, null=True, verbose_name='Picture')
    phone = models.CharField(max_length=15)
    college_id = models.CharField(max_length=20,unique=True,null=True)
    univeristy_name = models.CharField(max_length=30, choices=university, default='Zagazig_University')
    major_types = models.CharField(max_length=30, choices=major_types, default='electrical_engineering')
    facebook =models.URLField(max_length=200, blank=True)
    github =models.URLField(max_length=200, blank=True)
    linkedin =models.URLField(max_length=200, blank=True)
    # teacher = 'teacher'
    # student = 'student'
    # user_types = [
    #     (student, 'student'),
    #     (teacher, 'teacher'),
    # ]
    user_type = models.CharField(max_length=10, choices=user_types, default='student')
    points = models.PositiveIntegerField(default=0, verbose_name="points")
    def modify_points(self, added_points):
        self.points += added_points
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 250, 250

        if self.picture:
            pic = Image.open(self.picture.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.picture.path)

    def __str__(self):
        return self.user.username

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('index')


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)