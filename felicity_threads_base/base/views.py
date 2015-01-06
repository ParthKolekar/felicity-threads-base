from django.shortcuts import render

# Create your views here.
from base.models import Question, Submission

from django.http import HttpResponse

SUBMISSION_STATE_CHOICES = { 'WA': 'Wrong Answer', 'AC': 'Accepted', 'PR': 'Processing' }

def index(request):
    return render(request , 'base/index.html' , {'foo' : "bar"})

def problems(request):
    query_result = Question.objects.all()
    success_sub = Submission.objects.filter(submission_state='AC')
    problem_data = []
    for question in query_result:
        total = len(success_sub.filter(submission_question=question))
        problem_data.append([question.question_level, question.question_level_id, question.question_title, total])
    return render(request, 'base/problems.html', {'problem_data':problem_data})

def question(request, level, id):
    question_data = Question.objects.filter(question_level=level).filter(question_level_id=id);
    if len(question_data):
        question_details = question_data[0];
    else:
        question_details = 'none';
    return render(request, 'base/question.html', {'question_data':question_details})

def submissions(request):
    user_submissions = Submission.objects.filter(submission_user__user_username='admin').order_by('id')
    #replace admin by session variable for username
    user_submissions = user_submissions.reverse()
    for submit in user_submissions:
        submit.submission_state = SUBMISSION_STATE_CHOICES[submit.submission_state]
    return render(request, 'base/submissions.html', {'user_submissions':user_submissions})

