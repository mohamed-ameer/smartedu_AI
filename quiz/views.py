from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from classroom.models import Course,LeaderboardCourse
from quiz.forms import NewQuizForm, NewQuestionForm
from quiz.models import Answer, Question, Quizzes, Attempter, Attempt
from module.models import Module
from completion.models import Completion
from app_users.models import Profile
from scheduale.models import *
# Create your views here.

def NewQuiz(request, course_id, module_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        form = NewQuizForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            quiz = Quizzes.objects.create(user=user, title=title,start_time=start_time,end_time=end_time)
            module.quizzes.add(quiz)
            module.save()
            QuizScheduale.objects.create(user=user,course=course,module=module,quiz=quiz,title=title,start_time=start_time)   
            print('quiz scheduale done')         
            return redirect('new-question', course_id=course_id, module_id=module_id, quiz_id=quiz.id)
    else:
        form = NewQuizForm()

    context = {
        'form': form,'course': course
    }
    return render(request, 'quiz/newquiz.html', context)


def NewQuestion(request, course_id, module_id, quiz_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get('question_text')
            points = form.cleaned_data.get('points')
            answer_text = request.POST.getlist('answer_text')
            is_correct = request.POST.getlist('is_correct')

            question = Question.objects.create(question_text=question_text, user=user, points=points)

            for a, c in zip(answer_text, is_correct):
                answer = Answer.objects.create(answer_text=a, is_correct=c, user=user)
                question.answers.add(answer)
                question.save()
                quiz.questions.add(question)
                quiz.save()
            return redirect('new-question', course_id=course_id, module_id=module_id, quiz_id=quiz.id)
    else:
        form = NewQuestionForm()

    context = {
        'form': form,'course': course
    }
    return render(request, 'quiz/newquestion.html', context)


def QuizDetail(request, course_id, module_id, quiz_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    my_attempts = Attempter.objects.filter(quiz=quiz, user=user)

    context = {
        'quiz': quiz,
        'user': user,
        'my_attempts': my_attempts,
        'course_id': course_id,
        'module_id': module_id,
        'course': course,
        'module': module,
    }
    return render(request, 'quiz/quizdetail.html', context)

def TakeQuiz(request, course_id, module_id, quiz_id):
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    context = {
        'quiz': quiz,
        'course': course,
        'module': module,
        'course_id': course_id,
        'module_id': module_id,
    }
    return render(request, 'quiz/takequiz.html', context)


def SubmitAttempt(request, course_id, module_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    course = get_object_or_404(Course, id=course_id)
    earned_points = 0
    if request.method == 'POST':
        questions = request.POST.getlist('question')
        answers = request.POST.getlist('answer')
        attempter = Attempter.objects.create(user=user, quiz=quiz,course=course,score=0)

        for q, a in zip(questions, answers):
            question = Question.objects.get(id=q)
            answer = Answer.objects.get(id=a)
            Attempt.objects.create(quiz=quiz, attempter=attempter, question=question, answer=answer)
            Completion.objects.create(user=user, course_id=course_id, quiz=quiz)
            if answer.is_correct == True:
                earned_points += question.points
                attempter.score += earned_points
                attempter.save()
        points = earned_points
        LeaderboardCourse.objects.get(user=user,course=course).modify_points(points)
        Profile.objects.get(pk=user.id).modify_points(points)
        return redirect('quiz-detail',course_id=course_id,module_id=module_id,quiz_id=quiz_id)


def AttemptDetail(request, course_id, module_id, quiz_id, attempt_id):
    user = request.user
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    my_attempts = Attempter.objects.filter(quiz=quiz, user=user)
    attempts = Attempt.objects.filter(quiz=quiz, attempter__user=user)

    context = {
        'quiz': quiz,
        'course': course,
        'module': module,
        'my_attempts': my_attempts,
        'attempts': attempts,
        'course_id': course_id,
        'module_id': module_id,
    }
    return render(request, 'quiz/attemptdetail.html', context)
