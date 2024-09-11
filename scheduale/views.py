from django.shortcuts import render
from .models import *
# Create your views here.
def Scheduale(request):
    user =request.user
    assignments=AssignmentScheduale.objects.all()
    quizes=QuizScheduale.objects.all()
    context = {
        'assignments': assignments,'quizes': quizes,'user':user
    }    
    return render(request, 'classroom/Scheduale.html',context)
