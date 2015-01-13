from django.shortcuts import render
# Create your views here.
from django.contrib.auth.decorators import login_required
from base.models import User, ClarificationMessages
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

SUBMISSION_STATE_CHOICES = { 'WA': 'Wrong Answer', 'AC': 'Accepted', 'PR': 'Processing', 'NA': 'Not Attempted' }

@login_required
def index(request):
    profile = User.objects.filter(user_username = request.user.username)[0]
    if profile.user_notification_flash == True:
        message = "You have a new notification"
        profile.user_notification_flash = False
        profile.save()
    else:
        message = ""

    notifs = ClarificationMessages.objects.all().order_by('id').reverse()
    print notifs
    return render(request, 'cache_in/index.html', {'user_nick':profile.user_nick, 'notifs': notifs})

@login_required
def problems(request):
    profile = User.objects.filter(user_username = request.user.username)[0]
    query_result = Question.objects.filter(question_level__lte=profile.user_access_level).order_by('id')
    success_sub = Submission.objects.filter(submission_user__user_username = profile.user_username)
    problem_data = []
    for question in query_result:
        acc = success_sub.filter(submission_question=question).filter(submission_state='AC')
        wan = success_sub.filter(submission_question=question).filter(submission_state='WA')
        if acc:
            sta = SUBMISSION_STATE_CHOICES['AC']
        elif wan:
            sta = SUBMISSION_STATE_CHOICES['WA']
        else:
            sta = SUBMISSION_STATE_CHOICES['NA']
        problem_data.append([question.question_level, question.question_level_id, question.question_title, sta])
    return render(request, 'cache_in/problems.html', {'problem_data':problem_data, 'user_nick':profile.user_nick})

@login_required
def question(request, level, id):
    profile = User.objects.filter(user_username=request.user.username)[0]
    user_level = profile.user_access_level
    user_nick = profile.user_nick

    question_data = Question.objects.filter(question_level=level).filter(question_level_id=id)
    if len(question_data):
        if int(level) <= user_level:
            question_details = question_data[0]
            return render(request, 'cache_in/question.html', {'question_data':question_details, 'user_nick':user_nick})
        else:
            return render(request, 'cache_in/error.html', {'error_code': 1, 'user_nick':user_nick})
    else:
        return render(request, 'cache_in/error.html', {'error_code': 2, 'user_nick':user_nick})

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
    time_last = None
    time_last_query = Submission.objects.filter(submission_user__user_username=request.user.username).order_by('submission_timestamp').last()
    if time_last_query:
        time_last = time_last_query.submission_timestamp
    time_limit = datetime.timedelta(0, 30)
    print time_last, datetime.datetime.now(utc)
    if(time_last is None or time_last + time_limit <= datetime.datetime.now(utc)):
        ans_file = request.FILES.get("answer_file")
        #print ans_file, request.FILES
        ans_text = request.POST.get("answer_text")
        if ans_text and len(ans_text) > 255:
            # return HttpResponse(content = 'String too large.', status=413)
            return render(request, 'cache_in/error.html', {'error_code':3})
        question = Question.objects.filter(question_level=level).filter(question_level_id=id)
        user = User.objects.filter(user_username=request.user.username)[0]
        if len(question):
            question = question[0]
            submission = Submission(submission_question=question, submission_user=user, submission_string=ans_text, submission_storage=ans_file)
            ans = submission.__check_ans__()
            if(ans == 'AC' and int(level) == int(submission.submission_user.user_access_level)):
                print "Correct"
                submission.submission_user.level_up()
                submission.submission_user.score_up(100)
                submission.submission_user.save()
            submission.save()
    else:
        # return HttpResponse(content = 'Cannot submit before 30s of last submission.', status=403)
        return render(request, 'cache_in/error.html', {'error_code':4})
    return HttpResponseRedirect('/contest/cache_in/problems')

@login_required
def scoreboard(request):
    return render(request, 'cache_in/scoreboard.html')