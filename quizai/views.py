from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from classroom.models import Course
from quizai.forms import *
from quizai.models import *
from module.models import Module
from completion.models import Completion
from app_users.models import Profile
from scheduale.models import *
from .quiz_generator import *
# Create your views here.

def NewQuizAI(request, course_id, module_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        form = NewQuizForm(request.POST)
        if form.is_valid():
            context = form.cleaned_data.get('context')
            file = request.FILES.get('file')
            points = form.cleaned_data.get('points')
            quiz = QuizzesAI.objects.create(user=user, context=context, file=file, points=points)
            module.quizzes_ai.add(quiz)
            # questionsnlp,answers,wrong_options = nlp_model(context)
            questionsdl,keywords,distractors = dl_model(context)
            # print(nlp_model(context))
                     
            print(questionsdl)                 
            print('quiz ai done')         
            print(keywords)                 
            print('quiz ai done')         
            print(distractors)                 
            print('quiz ai done')    
            module.save()
            quiz5 = get_object_or_404(QuizzesAI, id=quiz.id)
            for i in range(len(questionsdl)):
                ques =QuestionAI.objects.create(question_text=questionsdl[i],points=points,user=user)
                ans =AnswerAI.objects.create(answer_text=keywords[i], is_correct=True, user=user)
                ques.answers.add(ans)
                for wr in distractors[i]:
                    ans =AnswerAI.objects.create(answer_text=wr, is_correct=False, user=user)
                    ques.answers.add(ans)
                ques.save()
                quiz5.questions.add(ques)
                quiz5.save()            
            return redirect('new-questionai', course_id=course_id, module_id=module_id, quiz_id=quiz.id)
    else:
        form = NewQuizForm()

    context = {
        'form': form,'course': course
    }
    return render(request, 'quizai/newquizai.html', context)


def NewQuestionAI(request, course_id, module_id, quiz_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(QuizzesAI, id=quiz_id)
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get('question_text')
            answer_text = request.POST.getlist('answer_text')
            is_correct = request.POST.getlist('is_correct')

            question = QuestionAI.objects.create(question_text=question_text, user=user)

            for a, c in zip(answer_text, is_correct):
                answer = AnswerAI.objects.create(answer_text=a, is_correct=c, user=user)
                question.answers.add(answer)
                question.save()
                quiz.questions.add(question)
                quiz.save()
            return redirect('new-questionai', course_id=course_id, module_id=module_id, quiz_id=quiz.id)
    else:
        form = NewQuestionForm()

    context = {
        'form': form,'course': course
    }
    return render(request, 'quizai/newquestionai.html', context)


def QuizDetailAI(request, course_id, module_id, quiz_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    quiz = get_object_or_404(QuizzesAI, id=quiz_id)
    my_attempts = AttempterAI.objects.filter(quiz=quiz, user=user)

    context = {
        'quiz': quiz,
        'user': user,
        'my_attempts': my_attempts,
        'course_id': course_id,
        'module_id': module_id,
        'course': course,
        'module': module,
    }
    return render(request, 'quizai/quizdetailai.html', context)

def TakeQuizAI(request, course_id, module_id, quiz_id):
    quiz = get_object_or_404(QuizzesAI, id=quiz_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    context = {
        'quiz': quiz,
        'course': course,
        'module': module,
        'course_id': course_id,
        'module_id': module_id,
    }
    return render(request, 'quizai/takequizai.html', context)


def SubmitAttemptAI(request, course_id, module_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(QuizzesAI, id=quiz_id)
    earned_points = 0
    if request.method == 'POST':
        questions = request.POST.getlist('question')
        answers = request.POST.getlist('answer')
        attempter = AttempterAI.objects.create(user=user, quiz=quiz, score=0)

        for q, a in zip(questions, answers):
            question = QuestionAI.objects.get(id=q)
            answer = AnswerAI.objects.get(id=a)
            AttemptAI.objects.create(quiz=quiz, attempter=attempter, question=question, answer=answer)
            # Completion.objects.create(user=user, course_id=course_id, quiz=quiz)
            if answer.is_correct == True:
                print("myanswer")
                earned_points += question.points
                attempter.score += earned_points
                attempter.save()
        points = earned_points
        Profile.objects.get(pk=user.id).modify_points(points)
        return redirect('quiz-detailai',course_id=course_id,module_id=module_id,quiz_id=quiz_id)


def AttemptDetailAI(request, course_id, module_id, quiz_id, attempt_id):
    user = request.user
    quiz = get_object_or_404(QuizzesAI, id=quiz_id)
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    my_attempts = AttempterAI.objects.filter(quiz=quiz, user=user)
    attempts = AttemptAI.objects.filter(quiz=quiz, attempter__user=user)

    context = {
        'quiz': quiz,
        'course': course,
        'module': module,
        'my_attempts': my_attempts,
        'attempts': attempts,
        'course_id': course_id,
        'module_id': module_id,
    }
    return render(request, 'quizai/attemptdetailai.html', context)
