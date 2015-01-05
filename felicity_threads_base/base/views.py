from django.shortcuts import render

# Create your views here.
from base.models import Question, Submission

from django.http import HttpResponse

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
    question_data = Question.objects.filter(question_level=level).filter(question_level_id=id)
    return render(request, 'base/question.html', {'question_data':question_data[0]})
