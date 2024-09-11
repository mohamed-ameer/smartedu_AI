from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from assignment.forms import NewAssignmentForm, NewSubmissionForm
from assignment.models import AssignmentFileContent, Assignment, Submission
from app_users.models import Profile
from module.models import Module
from classroom.models import Course, Grade,LeaderboardCourse
from completion.models import Completion
from scheduale.models import AssignmentScheduale
# marcoo
from difflib import SequenceMatcher as sm
import subprocess
import os
def executeJavaDoctor(fjava,fjavawithout):
   global Java_Output_doctor
   s = subprocess.getoutput(str("javac " + str(fjava) + ";java " +str(fjavawithout)))
   Java_Output_doctor=s
   print("Java_Output_doctor is : " + Java_Output_doctor)

def executeJavaStudent():
   global Java_Output_student
   #s = subprocess.check_output("javac SumOfNumbers2.java;java SumOfNumbers2",isinstance(input,int),subprocess.errno,stdin = data, shell = True)
   s = subprocess.getoutput("javac HelloWorldStudent.java;java HelloWorldStudent")
   Java_Output_student=s
   print("Java_Output_student is : " + Java_Output_student)  
# Driver function
if __name__=="__main__":
    executeJavaDoctor()
    executeJavaStudent()
    similarity=sm(None,Java_Output_doctor,Java_Output_student).ratio()
    Final_degree=similarity*5#point int(points) مكان ال 5
    print(Final_degree) #degree of student
# end marcoo
# Create your views here.
def NewAssignment(request, course_id, module_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    files_objs = []

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewAssignmentForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                points = form.cleaned_data.get('points')
                dead_time = form.cleaned_data.get('dead_time')
                assignment_type = form.cleaned_data.get('assignment_type')
                language_type = form.cleaned_data.get('language_type')
                # files = request.FILES.getlist('files')
                # for file in files:
                #     file_instance = AssignmentFileContent(file=file, user=user)
                #     file_instance.save()
                #     files_objs.append(file_instance)
                file = request.FILES.get('file')
                a = Assignment.objects.create(title=title, points=points,file=file,assignment_type=assignment_type ,language_type=language_type,dead_time=dead_time, user=user)
                # a.files.set(files_objs)
                a.save()
                module.assignments.add(a)
                AssignmentScheduale.objects.create(user=user,course=course,module=module,assignment=a,title=title,due=dead_time)
                print('scheduale object done')
                if a.assignment_type == 'Programming_File' and a.language_type == 'Java':
                    # marcoo functions
                    filejava=os.path.basename(file.name)#HelloWorldDoctor.java
                    filejavawithoutext=os.path.splitext(filejava)[0] #HelloWorldDoctor
                    executeJavaDoctor(filejava,filejavawithoutext)
                    print(filejavawithoutext)
                return redirect('modules', course_id=course_id)
        else:
            form = NewAssignmentForm()
    
    context = {
        'form': form,'course': course
    }
    return render(request, 'assignment/newassignment.html', context)

# Edit assignment

# 
def AssignmentDetail(request, course_id, module_id, assignment_id):
    user = request.user
    module = get_object_or_404(Module, id=module_id)
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id)
    my_submissions = Submission.objects.filter(assignment=assignment, user=user)

    context = {
        'assignment': assignment,
        'course': course,
        'course_id': course_id,
        'my_submissions': my_submissions,
        'course_id': course_id,
        'module_id': module_id,
        'module': module,
    }
    return render(request, 'assignment/assignment.html', context)

def NewSubmission(request, course_id, module_id, assignment_id):
    user = request.user
    module = get_object_or_404(Module, id=module_id)
    assignment = get_object_or_404(Assignment, id=assignment_id)
    my_submissions = Submission.objects.filter(assignment=assignment, user=user)
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = NewSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('file')
            comment = form.cleaned_data.get('comment')
            s = Submission.objects.create(file=file, comment=comment, user=user, assignment=assignment)
            Grade.objects.create(course=course, submission=s)
            Completion.objects.create(user=user, course=course, assignment=assignment)
            points = 1
            Profile.objects.get(pk=user.id).modify_points(points)
            return redirect('modules', course_id=course_id)
    else:
        form = NewSubmissionForm()
    context = {
        'form': form,
        'course': course,
        'course_id': course_id,
        'module_id': module_id,
        'my_submissions': my_submissions,
        'assignment_id': assignment_id,
        'module': module,
        'assignment': assignment,
    }
    return render(request, 'assignment/submitassignment.html', context)
