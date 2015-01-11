from django.shortcuts import render
# Create your views here.
from django.contrib.auth.decorators import login_required
from base.models import User
from cache_in.models import Question, Submission
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import datetime

class UTC(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(0)
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return datetime.timedelta(0)

utc = UTC()

SUBMISSION_STATE_CHOICES = { 'WA': 'Wrong Answer', 'AC': 'Accepted', 'PR': 'Processing' }

@login_required
def index(request):
    st = ""
    for i in request.session.items():
        st += str(i)
    st += request.user.username
    return HttpResponse(st)
#    return render(request , 'base/index.html' , {'foo' : "bar"})

@login_required
def problems(request):
    query_result = Question.objects.all()
    success_sub = Submission.objects.filter(submission_state='AC')
    problem_data = []
    for question in query_result:
        total = len(success_sub.filter(submission_question=question))
        problem_data.append([question.question_level, question.question_level_id, question.question_title, total])
    return render(request, 'cache_in/problems.html', {'problem_data':problem_data})

@login_required
def question(request, level, id):
    user_level = User.objects.filter(user_username=request.user.username)[0].user_access_level
    if(int(level) <= user_level):
        question_data = Question.objects.filter(question_level=level).filter(question_level_id=id)
        if len(question_data):
            question_details = question_data[0];
        else:
            question_details = None;
    else:
        question_details = None;
    return render(request, 'cache_in/question.html', {'question_data':question_details})

@login_required
def submissions(request):
    user_submissions = Submission.objects.filter(submission_user__user_username=request.user.username).order_by('id')
    user_submissions = user_submissions.reverse()
    for sub in user_submissions:
        sub.submission_state = SUBMISSION_STATE_CHOICES[sub.submission_state]
    return render(request, 'cache_in/submissions.html', {'user_submissions':user_submissions})

@login_required
def submit(request, level, id):
    context = RequestContext(request)
    #print request.method
    time_last = Submission.objects.filter(submission_user__user_username=request.user.username).order_by('submission_timestamp').last().submission_timestamp
    time_limit = datetime.timedelta(0, 30)
    print time_last, datetime.datetime.now(utc)
    if(time_last + time_limit <= datetime.datetime.now(utc)):
        ans_file = request.FILES.get("answer_file")
        #print ans_file, request.FILES
        ans_text = request.POST.get("answer_text")
        if ans_text and len(ans_text) > 255:
            return HttpResponse(content = 'String too large.', status=413)
        question = Question.objects.filter(question_level=level).filter(question_level_id=id)
        user = User.objects.filter(user_username=request.user.username)[0]
        if len(question):
            question = question[0]
            submission = Submission(submission_question=question, submission_user=user, submission_string=ans_text, submission_storage=ans_file)
            ans = submission.__check_ans__()
            if(ans == 'AC' and level == submission.submission_user.user_access_level):
                print "Correct"
                submission.submission_user.level_up()
                submission.submission_user.score_up(100)
                submission.submission_user.save()
            submission.save()
    else:
        return HttpResponse(content = 'Cannot submit before 30s of last submission.', status=403)
    return HttpResponseRedirect('/cache_in/submissions')