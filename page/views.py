from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from page.models import Page, PostFileContent,Comment, Reply
from classroom.models import Course
from app_users.models import Profile
from module.models import Module
from completion.models import Completion

from page.forms import NewPageForm

# Create your views here.

@login_required
def NewPageModule(request, course_id, module_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    files_objs = []

    if user != course.user:
        return HttpResponseForbidden()

    else:
        if request.method == 'POST':
            form = NewPageForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                video_url = form.cleaned_data.get('video_url')
                description = form.cleaned_data.get('description')
                file = request.FILES.get('file')
                # files = request.FILES.getlist('files')
                # for file in files:
                #     file_instance = PostFileContent(file=file, user=user)
                #     file_instance.save()
                #     files_objs.append(file_instance)

                p = Page.objects.create(title=title,file=file,video_url=video_url,description=description, user=user)
                # p.files.set(files_objs)
                p.save()
                module.pages.add(p)
                return redirect('modules', course_id=course_id)
        else:
            form = NewPageForm()
    context = {
        'form': form,'course': course
    }

    return render(request, 'page/newpage.html', context)

# Edit page
@login_required
def EditPage(request, course_id, module_id,page_id):
    user = request.user
    page = get_object_or_404(Page, id=page_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    files_objs = []    
    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewPageForm(request.POST, request.FILES,instance=page)
            if form.is_valid():
                page.title = form.cleaned_data.get('title')
                page.video_url = form.cleaned_data.get('video_url')
                page.description = form.cleaned_data.get('description')
                page.file = request.FILES.get('file')
                # page.files = request.FILES.getlist('files')
                # for file in page.files:
                #     file_instance = PostFileContent(file=file, user=user)
                #     file_instance.save()
                #     files_objs.append(file_instance)
                page.save()
                return redirect('modules', course_id=course_id)
        else:
            form = NewPageForm()

    context = {
        'form': form,
        'course': course,
        'module':module,
    }

    return render(request, 'classroom/editpage.html', context)


# 
def PageDetail(request, course_id, module_id, page_id):
    user=request.user    
    page = get_object_or_404(Page, id=page_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    completed = Completion.objects.filter(course_id=course_id, user=request.user, page_id=page_id).exists()

    if request.method == 'POST':
        comm = request.POST.get('comm')
        comm_id = request.POST.get('comm_id') #None

        if comm_id:
            Reply(page=page,
                    user = request.user,
                    comm = comm,
                    comment= Comment.objects.get(id=int(comm_id))
                ).save()
        else:
            Comment(page=page, user=request.user, comm=comm).save()
        points = 1
        Profile.objects.get(pk=user.id).modify_points(points)



    comments = []
    for c in Comment.objects.filter(page=page):
        comments.append([c, Reply.objects.filter(comment=c)])
    context = {
        'comments':comments,
        'page': page,
        'course': course,
        'module': module,
        'completed': completed,
        'course_id': course_id,
        'module_id': module_id,
        'page_id': page_id,
    }
    return render(request, 'page/page.html', context)


def MarkPageAsDone(request, course_id, module_id, page_id):
    user = request.user
    page = get_object_or_404(Page, id=page_id)
    course = get_object_or_404(Course, id=course_id) 
    Completion.objects.create(user=user, course=course, page=page)
    points = 1
    Profile.objects.get(pk=user.id).modify_points(points)
    return redirect('modules', course_id=course_id)

