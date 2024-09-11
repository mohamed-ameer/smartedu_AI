from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def user_directory_path(instance, filename):
	#THis file will be uploaded to MEDIA_ROOT /the user_(id)/the file
	return 'user_{0}/{1}'.format(instance.user.id, filename)

class AnswerAI(models.Model):
    answer_text = models.CharField(max_length=900)
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text

class QuestionAI(models.Model):
    question_text = models.CharField(max_length=900)
    answers = models.ManyToManyField(AnswerAI)
    points = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class QuizzesAI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    context=models.TextField(blank=True) 
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)   
    points = models.PositiveIntegerField()
    questions = models.ManyToManyField(QuestionAI)

    def __str__(self):
        return self.user.username

class AttempterAI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizzesAI, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    completed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class AttemptAI(models.Model):
    quiz = models.ForeignKey(QuizzesAI, on_delete=models.CASCADE)
    attempter = models.ForeignKey(AttempterAI, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionAI, on_delete=models.CASCADE)
    answer = models.ForeignKey(AnswerAI, on_delete=models.CASCADE)

    def __str__(self):
        return self.attempter.user.username + ' - ' + self.answer.answer_text


