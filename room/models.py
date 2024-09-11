from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Create your models here.
class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_owner')
    course = models.ForeignKey(to='classroom.Course', on_delete=models.CASCADE)    
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(null=True, blank=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Message(models.Model):
    room=models.ForeignKey(Room,related_name='messages',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='messages',on_delete=models.CASCADE)
    content =models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('date_added',)

        