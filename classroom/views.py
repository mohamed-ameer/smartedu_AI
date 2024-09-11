from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden,HttpResponse
from app_users.models import Profile
from classroom.models import Course, Category,Grade,LeaderboardCourse
from app_users.models import *
from classroom.forms import NewCourseForm
from .filters import *
from assignment.filters import *
from quiz.models import Attempter
# Create your views here.

@login_required
def index(request):
    user = request.user
    courses = Course.objects.filter(enrolled=user)

    context = {
        'courses': courses
    }
    return render(request, 'index.html', context)

def Categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'classroom/categories.html', context)

# def Scheduale(request):

#     return render(request, 'classroom/Scheduale.html')
def Activity(request):
    user = request.user
    courses = Course.objects.filter(enrolled=user)

    context = {
        'courses': courses
    }
    return render(request, 'classroom/Activity.html', context)
def Leaderboard(request):
    profiles =Profile.objects.all().filter(user_type='student').order_by("-points")
    myFilter=ProfileFilter(request.GET,queryset=profiles)
    profiles =myFilter.qs
    context = {
        'profiles': profiles,'myFilter':myFilter
    }
    return render(request, 'classroom/Leaderboard.html', context)

def Leaderboardreverse(request):
    profiles =Profile.objects.all().filter(user_type='student').order_by("points")
    myFilter=ProfileFilter(request.GET,queryset=profiles)
    profiles =myFilter.qs
    context = {
        'profiles': profiles,'myFilter':myFilter
    }
    return render(request, 'classroom/Leaderboardreverse.html', context)
def Leaderboardeachcourse(request,course_id):
    course = get_object_or_404(Course, id=course_id)
    leaders =LeaderboardCourse.objects.all().filter(course=course).order_by("-points")
    context = {
        'leaders': leaders,'course': course
    }
    return render(request, 'classroom/Leaderboardcourse.html', context)

def CategoryCourses(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    courses = Course.objects.filter(category=category)

    context = {
        'category': category,
        'courses': courses,
    }
    return render(request, 'classroom/categorycourses.html', context)


def NewCourse(request):
    user = request.user
    if request.method == 'POST':
        form = NewCourseForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            title = form.cleaned_data.get('title')
            secret_code = form.cleaned_data.get('secret_code')
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            Course.objects.create(picture=picture, title=title,secret_code=secret_code,description=description, category=category, user=user)
            return redirect('my-courses')
    else:
        form = NewCourseForm()

    context = {
        'form': form,
    }

    return render(request, 'classroom/newcourse.html', context)


@login_required
def CourseDetail(request, course_id):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    course = get_object_or_404(Course, id=course_id)
    context = {
        'course': course,'profile': profile
    }

    return render(request, 'classroom/course.html', context)

@login_required
def Enroll(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    code=request.POST.get('code')
    print(code)
    if code == course.secret_code:
        course.enrolled.add(user)
        LeaderboardCourse.objects.create(user=user,course=course)
    else:
        return HttpResponse("Please enter the correct secret key of the course,if you don't know ask your instructor")
    return redirect('activity')

@login_required
def DeleteCourseWarning(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        context = {
        'course': course,
        }
    return render(request, 'classroom/deletewarning.html', context)
@login_required
def DeleteCourse(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        course.delete()
    return redirect('my-courses')


@login_required
def EditCourse(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()

    else:
        if request.method == 'POST':
            form = NewCourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                course.picture = form.cleaned_data.get('picture')
                course.title = form.cleaned_data.get('title')
                course.secret_code = form.cleaned_data.get('secret_code')
                course.description = form.cleaned_data.get('description')
                course.category = form.cleaned_data.get('category')
                course.save()
                return redirect('my-courses')
        else:
            form = NewCourseForm(instance=course)

    context = {
        'form': form,
        'course': course
    }

    return render(request, 'classroom/editcourse.html', context)


def MyCourses(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    courses = Course.objects.filter(user=user)

    context = {
        'courses': courses,'profile': profile
    }

    return render(request, 'classroom/mycourses.html', context)
# all courses ########################################
@login_required
def AllCourses(request):
    user = request.user
    courses = Course.objects.all()
    myFilter=CourseFilter(request.GET,queryset=courses)
    courses =myFilter.qs
    return render(request, 'classroom/allcourses.html', {'courses': courses,'user':user,'myFilter':myFilter})
# ##############################################################

def Submissions(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    grades = Grade.objects.filter(course=course, submission__user=user)
    context = {
        'grades': grades,
        'course': course
    }
    return render(request, 'classroom/submissions.html', context)

def StudentSubmissions(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    if user != course.user:
        return HttpResponseForbidden()
    else:
        grades = Grade.objects.filter(course=course)
        myFilter=GradeFilter(request.GET,queryset=grades)
        grades =myFilter.qs
        context = {
            'course': course,
            'grades': grades,
            'myFilter': myFilter,
        }
    return render(request,'classroom/studentgrades.html', context)
def StudentQuizSubmissions(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    if user != course.user:
        return HttpResponseForbidden()
    else:
        attempts = Attempter.objects.filter(course=course)
        context = {
            'course': course,
            'attempts': attempts,
        }
    return render(request,'classroom/studentquizgrades.html', context)

def GradeSubmission(request, course_id, grade_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    grade = get_object_or_404(Grade, id=grade_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            points = request.POST.get('points')
            grade.points = points
            grade.status = 'graded'
            grade.graded_by = user
            grade.save()
            LeaderboardCourse.objects.get(user=grade.submission.user,course=course).modify_points(int(points))
            Profile.objects.get(pk=grade.submission.user.id).modify_points(int(points))
            return redirect('student-submissions', course_id=course_id)
    context = {
        'course': course,
        'grade': grade,
    }

    return render(request, 'classroom/gradesubmission.html', context)

