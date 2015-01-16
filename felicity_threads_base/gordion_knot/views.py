from django.shortcuts import render
# Create your views here.
from django.contrib.auth.decorators import login_required
from base.models import User, ClarificationMessages
from gordion_knot.models import Question, Submission, Comment
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

# TIME_SINCE_MY_BIRTH = datetime.datetime(2015,1,1,1,1,1,1,utc)

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
    return render(request, 'gordion_knot/index.html', {'user_nick':profile.user_nick, 'notifs': notifs})

@login_required
def problems(request):
    profile = User.objects.filter(user_username = request.user.username)[0]
    query_result = Question.objects.filter(question_level__lte=profile.user_access_level).order_by('question_level').order_by('question_level_id')
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
    return render(request, 'gordion_knot/problems.html', {'problem_data':problem_data, 'user_nick':profile.user_nick})

@login_required
def question(request, level, id):
    question_comments = None
    profile = User.objects.filter(user_username=request.user.username)[0]
    user_level = profile.user_access_level
    user_nick = profile.user_nick
    question_data = Question.objects.filter(question_level=level).filter(question_level_id=id)
    if len(question_data):
        question_comments = Comment.objects.filter(comment_question=question_data).filter(comment_is_approved=True).order_by('comment_timestamp')
        if int(level) <= user_level:
            question_details = question_data[0]
            return render(request, 'gordion_knot/question.html', {'question_data':question_details, 'user_nick':user_nick, 'question_comments':question_comments})
        else:
            return render(request, 'base/error.html', {'error_code': 1, 'user_nick':user_nick})
    else:
        return render(request, 'base/error.html', {'error_code': 2, 'user_nick':user_nick})

@login_required
def submissions(request):
    user_submissions = Submission.objects.filter(submission_user__user_username=request.user.username).order_by('id')
    user_submissions = user_submissions.reverse()
    for sub in user_submissions:
        sub.submission_state = SUBMISSION_STATE_CHOICES[sub.submission_state]
    return render(request, 'gordion_knot/submissions.html', {'user_submissions':user_submissions})

@login_required
def submit(request, level, id):
    context = RequestContext(request)
    #print request.method
    time_last = None
    time_last_query = Submission.objects.filter(submission_user__user_username=request.user.username).filter(submission_state='WA').order_by('submission_timestamp').last()
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
            return render(request, 'base/error.html', {'error_code':3})
        question = Question.objects.filter(question_level=level).filter(question_level_id=id)
        user = User.objects.filter(user_username=request.user.username)[0]
        if len(question):
            question = question[0]
            submission = Submission(submission_question=question, submission_user=user, submission_string=ans_text, submission_storage=ans_file)
            ans = submission.__check_ans__()
            level_acc_question_ids_query = Submission.objects.filter(submission_user__user_username=request.user.username).filter(submission_question__question_level=level).filter(submission_state='AC').values('submission_question').distinct()
            print level_acc_question_ids_query
            level_acc_question_ids = []
            for questions in level_acc_question_ids_query:
                level_acc_question_ids.append(questions['submission_question'])
            if(ans == 'AC' and int(level) <= int(submission.submission_user.user_access_level) and long(id) not in level_acc_question_ids):
                print "Correct"
                submission.submission_user.level_up()
                submission.submission_user.score_up(int(level)*100)
                submission.submission_user.save()
            submission.save()
    else:
        # return HttpResponse(content = 'Cannot submit before 30s of last submission.', status=403)
        return render(request, 'base/error.html', {'error_code':4})
    return HttpResponseRedirect('/contest/gordion_knot/problems')

@login_required
def comment_submit(request, level, id):
    context = RequestContext(request)
    #print request.method
    time_last = None
    time_last_query = Comment.objects.filter(comment_user__user_username=request.user.username).order_by('comment_timestamp').last()
    if time_last_query:
        time_last = time_last_query.comment_timestamp
    time_limit = datetime.timedelta(0, 30)
    print time_last, datetime.datetime.now(utc)
    if(time_last is None or time_last + time_limit <= datetime.datetime.now(utc)):
        comment_text = request.POST.get("comment_text")
        if comment_text and len(comment_text) > 255:
            return render(request, 'base/error.html', {'error_code':3})
        question = Question.objects.filter(question_level=level).filter(question_level_id=id)
        user = User.objects.filter(user_username=request.user.username)[0]
        if len(question):
            question = question[0]
            comment = Comment(comment_question=question, comment_user=user, comment_message=comment_text)
            comment.save()
    else:
        return render(request, 'base/error.html', {'error_code':5})
    return HttpResponseRedirect('/contest/gordion_knot/question/'+level+'/'+id)


@login_required
def scoreboard(request):
    profile = User.objects.filter(user_username = request.user.username)[0]
    user_nick = profile.user_nick
    return render(request, 'gordion_knot/scoreboard.html',  {'user_nick':user_nick})
