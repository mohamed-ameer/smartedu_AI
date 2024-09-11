from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from embed_video.fields import EmbedVideoField
import os


# Create your models here.
def user_directory_path(instance, filename):
    #THis file will be uploaded to MEDIA_ROOT /the user_(id)/the file
    return 'user_files_{0}/{1}'.format(instance.user.id, filename)

class PostFileContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    posted = models.DateTimeField(auto_now_add=True)

    def get_file_name(self):
        return os.path.basename(self.file.name)

class Page(models.Model):
    title = models.CharField(max_length=150)
    video_url = EmbedVideoField()
    description = models.CharField(max_length=300)
    # files = models.ManyToManyField(PostFileContent)
    file = models.FileField(upload_to=user_directory_path, blank=False)   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page_owner')
    def get_file_name(self):
        return os.path.basename(self.file.name)
    def __str__(self):
        return self.title

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    page=models.ForeignKey(Page,on_delete=models.CASCADE)
    comm=models.TextField()
    time=models.DateTimeField(auto_now_add=True,auto_now=False)
    def __str__(self):
        return self.comm
class Reply(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    page=models.ForeignKey(Page,on_delete=models.CASCADE,null=True)
    comm=models.TextField()
    time=models.DateTimeField(auto_now_add=True,auto_now=False)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    def __str__(self):
        return self.comm