from django.shortcuts import render

# Create your views here.
from base.models import Question, Submission, User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

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
        question_details = None;
    return render(request, 'base/question.html', {'question_data':question_details})

def submissions(request):
    user_submissions = Submission.objects.filter(submission_user__user_username='admin').order_by('id')
    #replace admin by session variable for username
    user_submissions = user_submissions.reverse()
    for sub in user_submissions:
        sub.submission_state = SUBMISSION_STATE_CHOICES[sub.submission_state]
    return render(request, 'base/submissions.html', {'user_submissions':user_submissions})

def submit(request, level, id):
    context = RequestContext(request)
    #print request.method
    ans_file = request.FILES.get("answer_file")
    #print ans_file, request.FILES
    ans_text = request.POST.get("answer_text")
    question = Question.objects.filter(question_level=level).filter(question_level_id=id)
    user = User.objects.filter(user_username='admin')[0] #replace admin with the session variable for username
    if len(question):
        question = question[0]
        submission = Submission(submission_question=question, submission_user=user, submission_string=ans_text, submission_storage=ans_file)
        submission.__check_ans__()
        submission.save()
    return HttpResponseRedirect('/base/submissions')
