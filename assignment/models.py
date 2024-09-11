from django.db import models
from django.contrib.auth.models import User

import os

# Create your models here.


def user_directory_path(instance, filename):
    #THis file will be uploaded to MEDIA_ROOT /the user_(id)/the file
    return 'user_{0}/{1}'.format(instance.user.id, filename)
def student_directory_path(instance, filename):
    #THis file will be uploaded to MEDIA_ROOT /the user_(id)/the file
    return 'student_files/{0}'.format( filename)

class AssignmentFileContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)

    def get_file_name(self):
        return os.path.basename(self.file.name)

assignment_type = (
    ('Regular_File', 'Regular_File'),
    ('Programming_File', 'Programming_File'),
)
language_type = (
    ('None', 'None'),
    ('C', 'C'),
    ('C++', 'C++'),
    ('Java', 'Java'),
    ('Python', 'Python'),
)

class Assignment(models.Model):
    title = models.CharField(max_length=150)
    points = models.PositiveIntegerField()
    assignment_type = models.CharField(max_length=30, choices=assignment_type, default='Regular_File')
    language_type = models.CharField(max_length=30, choices=language_type, default='None')
    dead_time=models.DateTimeField()
    # files = models.ManyToManyField(AssignmentFileContent)
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_file_name(self):
        return os.path.basename(self.file.name)
    def __str__(self):
        return self.title

class Submission(models.Model):
    file = models.FileField(upload_to=student_directory_path)
    assignment_type = models.CharField(max_length=30, choices=assignment_type, default='Regular_File')
    language_type = models.CharField(max_length=30, choices=language_type, default='None')
    comment = models.CharField(max_length=1000,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_file_name(self):
        return os.path.basename(self.file.name)
    def __str__(self):
        return self.assignment.title
