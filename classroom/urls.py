from django.urls import path
from classroom.views import Categories, CategoryCourses, NewCourse, Enroll, DeleteCourse, EditCourse, MyCourses, CourseDetail, Submissions, StudentSubmissions, GradeSubmission,AllCourses
from classroom.views import *

from module.views import NewModule, CourseModules
from scheduale.views import Scheduale
from page.views import *
from quiz.views import NewQuiz, NewQuestion, QuizDetail, TakeQuiz, SubmitAttempt, AttemptDetail
from quizai.views import NewQuizAI, NewQuestionAI, QuizDetailAI, TakeQuizAI, SubmitAttemptAI, AttemptDetailAI
from assignment.views import NewAssignment, AssignmentDetail, NewSubmission
from question.views import NewStudentQuestion, Questions, QuestionDetail, MarkAsAnswer, VoteAnswer

urlpatterns = [

	#Course - Classroom Views
	path('newcourse/', NewCourse, name='newcourse'),
	path('MyCourses/', MyCourses, name='my-courses'),
	path('AllCourses/', AllCourses, name='all-courses'),
	path('categories/', Categories, name='categories'),
	path('scheduale/', Scheduale, name='scheduale'),
	path('leaderboard/', Leaderboard, name='leaderboard'),
	path('leaderboardreverse/', Leaderboardreverse, name='leaderboardreverse'),
	path('<course_id>/leaderboardcourse', Leaderboardeachcourse, name='leaderboardcourse'),
	path('activity/', Activity, name='activity'),
	path('categories/<category_slug>', CategoryCourses, name='category-courses'),
	path('<course_id>/', CourseDetail, name='course'),
	path('<course_id>/enroll', Enroll, name='enroll'),
	path('<course_id>/edit', EditCourse, name='edit-course'),
	path('<course_id>/deletewarning', DeleteCourseWarning, name='delete-course-warning'),
	path('<course_id>/delete', DeleteCourse, name='delete-course'),
	# #Modules
	path('<course_id>/modules', CourseModules, name='modules'),
	path('<course_id>/modules/newmodule', NewModule, name='new-module'),
	#Pages
	path('<course_id>/modules/<module_id>/pages/newpage', NewPageModule, name='new-page'),
	path('<course_id>/modules/<module_id>/pages/<page_id>', PageDetail, name='page-detail'),
	path('<course_id>/modules/<module_id>/pages/<page_id>/done', MarkPageAsDone, name='mark-page-as-done'),
	path('<course_id>/modules/<module_id>/pages/<page_id>/editpage', EditPage, name='editage'),
	# #Quizzes
	path('<course_id>/modules/<module_id>/quiz/newquiz', NewQuiz, name='new-quiz'),
	path('<course_id>/modules/<module_id>/quiz/<quiz_id>/newquestion', NewQuestion, name='new-question'),
	path('<course_id>/modules/<module_id>/quiz/<quiz_id>/', QuizDetail, name='quiz-detail'),
	path('<course_id>/modules/<module_id>/quiz/<quiz_id>/take', TakeQuiz, name='take-quiz'),
	path('<course_id>/modules/<module_id>/quiz/<quiz_id>/take/submit', SubmitAttempt, name='submit-quiz'),
	path('<course_id>/modules/<module_id>/quiz/<quiz_id>/<attempt_id>/results', AttemptDetail, name='attempt-detail'),
	# #Quizzes_ai
	path('<course_id>/modules/<module_id>/quiz/newquizai', NewQuizAI, name='new-quizai'),
	path('<course_id>/modules/<module_id>/quiz/<quiz_id>/newquestionai', NewQuestionAI, name='new-questionai'),
	path('<course_id>/modules/<module_id>/quiz/<quiz_id>/detailai', QuizDetailAI, name='quiz-detailai'),
	path('<course_id>/modules/<module_id>/quiz/<quiz_id>/takeai', TakeQuizAI, name='take-quizai'),
	path('<course_id>/modules/<module_id>/quiz/<quiz_id>/takeai/submitai', SubmitAttemptAI, name='submit-quizai'),
	path('<course_id>/modules/<module_id>/quiz/<quiz_id>/<attempt_id>/resultsai', AttemptDetailAI, name='attempt-detailai'),
	# #Assignment
	path('<course_id>/modules/<module_id>/assignment/newassignment', NewAssignment, name='new-assignment'),
	path('<course_id>/modules/<module_id>/assignment/<assignment_id>', AssignmentDetail, name='assignment-detail'),
	path('<course_id>/modules/<module_id>/assignment/<assignment_id>/start', NewSubmission, name='start-assignment'),
	# #Submissions
	path('<course_id>/submissions', Submissions, name='submissions'),
	path('<course_id>/studentsubmissions', StudentSubmissions, name='student-submissions'),
	path('<course_id>/studentquizsubmissions', StudentQuizSubmissions, name='student-quiz-submissions'),
	path('<course_id>/submissions/<grade_id>/grade', GradeSubmission, name='grade-submission'),
	#Questions
	path('<course_id>/questions', Questions, name='questions'),
	path('<course_id>/questions/newquestion', NewStudentQuestion, name='new-student-question'),
	path('<course_id>/questions/<question_id>', QuestionDetail, name='question-detail'),
	path('<course_id>/questions/<question_id>/vote', VoteAnswer, name='vote-answer'),
	path('<course_id>/questions/<question_id>/<answer_id>/markasanswer', MarkAsAnswer, name='mark-as-answer'),

]