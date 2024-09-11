from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid

# Create your models here.
from assignment.models import Submission
from question.models import Question

#3rd apps field
from ckeditor.fields import RichTextField

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('graded', 'Graded'),
)
#########################################################################
#save pictures and files in media folder with user_id
def user_directory_path(instance, filename):
    #THis file will be uploaded to MEDIA_ROOT /the user_(id)/the file
    return 'user_{0}/{1}'.format(instance.user.id, filename)
###########################################################################
# category
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    icon = models.CharField(max_length=100, verbose_name='Icon', default='article')
    slug = models.SlugField(unique=True)
    def get_absolute_url(self):
        return reverse('categories', arg=[self.slug])
    def __str__(self):
        return self.title
###########################################################################
# to know about UUID[https://www.techtarget.com/searchapparchitecture/definition/UUID-Universal-Unique-Identifier]
# it is very unique as same as your fingerprint


university = (
    ('Zagazig_University', 'Zagazig _University'),
    ('Cairo_University', 'Cairo_University'),
    ('Ain_Shams_University', 'Ain_Shams_University'),
)
major_types = (
    ('civil_engineering', 'civil_engineering'),
    ('chemical_engineering', 'chemical_engineering'),
    ('mechanical_engineering', 'mechanical_engineering'),
    ('electrical_engineering', 'electrical_engineering'),
    ('industrial_engineering', 'industrial_engineering'),
)

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path)
    title = models.CharField(max_length=200)
    secret_code = models.CharField(max_length=300,unique=True,null=True)
    description = models.CharField(max_length=300)
    university = models.CharField(max_length=30, choices=university, default='Zagazig_University')
    major_types = models.CharField(max_length=30, choices=major_types, default='electrical_engineering')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # many courses created by one user(teacher)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_owner')
    # many courses can enrolled by many users(studebt)
    enrolled = models.ManyToManyField(User)
    modules = models.ManyToManyField(to='module.Module')
    questions = models.ManyToManyField(Question)
    def __str__(self):
        return self.title

class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    graded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=10, verbose_name='Status')
class Enroll(models.Model):
    code = models.CharField(max_length=300)
class LeaderboardCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboardcourse')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0, verbose_name="points")
    def modify_points(self, added_points):
        self.points += added_points
        self.save()	
    def __str__(self):
        return self.user.username