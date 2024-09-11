from django.db import models
from django.contrib.auth.models import User
from classroom.models import Course
from module.models import Module
from assignment.models import Assignment
from quiz.models import Quizzes
# Create your models here.
class AssignmentScheduale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    module=models.ForeignKey(Module, on_delete=models.CASCADE)    
    assignment=models.ForeignKey(Assignment, on_delete=models.CASCADE)    
    title = models.CharField(max_length=150)
    due = models.DateField()
    def __str__(self):
        return self.title
class QuizScheduale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    module=models.ForeignKey(Module, on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    start_time=models.DateTimeField()
    def __str__(self):
        return self.title

