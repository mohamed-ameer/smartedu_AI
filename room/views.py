from email import message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Message, Room
from classroom.models import Course
from .forms import RoomForm
from .filters import RoomFilter
@login_required
def rooms(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    rooms = Room.objects.filter(course=course)
    myFilter=RoomFilter(request.GET,queryset=rooms)
    rooms =myFilter.qs
    return render(request, 'room/rooms.html', {'rooms': rooms,'course':course,'myFilter':myFilter})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages=Message.objects.filter(room=room)[0:25]
    return render(request, 'room/room.html', {'room': room,'messages': messages})


def NewRoom(request,course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            Room.objects.create(name=name,user=user,course=course)
            return redirect('rooms', course_id=course_id)
    else:
        form = RoomForm()
    
    context = {
        'form': form,'course':course
    }

    return render(request, 'room/newroom.html', context)
