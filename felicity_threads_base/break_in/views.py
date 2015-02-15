from django.shortcuts import render
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from base.models import User, ClarificationMessages
from break_in.models import Question, Submission, Comment, Team, TeamUser
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db import IntegrityError
import logging
import datetime

class UTC(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(0)
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return datetime.timedelta(0)

utc = UTC()
logger = logging.getLogger(__name__)
# TIME_SINCE_MY_BIRTH = datetime.datetime(2015,1,1,1,1,1,1,utc)

SUBMISSION_STATE_CHOICES = { 'WA': 'Wrong Answer', 'AC': 'Accepted', 'PR': 'Processing', 'NA': 'Not Attempted' }

@login_required
def csrf_failure(request, reason=""):
    profile = User.objects.filter(user_username = request.user.username)[0]
    return render(request, 'base/error.html' , {'user_nick' : profile.user_nick , 'error_code': 7}, status = 403)

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
    return render(request, 'break_in/index.html', {'user_nick':profile.user_nick, 'notifs': notifs})

@login_required
def problems(request):
    profile = User.objects.filter(user_username = request.user.username)[0]
    if request.user.is_staff:
        query_result = Question.objects.all().order_by('question_level_id').order_by('question_level')
    else:
        query_result = Question.objects.filter(question_level__lte=profile.user_access_level).order_by('question_level_id').order_by('question_level')
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
    return render(request, 'break_in/problems.html', {'problem_data':problem_data, 'user_nick':profile.user_nick})

@login_required
def question(request, level, id):
    question_comments = None
    profile = User.objects.filter(user_username=request.user.username)[0]
    user_level = profile.user_access_level
    user_nick = profile.user_nick
    question_data = Question.objects.filter(question_level=level).filter(question_level_id=id)
    if len(question_data):
        question_comments = Comment.objects.filter(comment_question=question_data).filter(comment_is_approved=True).order_by('comment_timestamp')
        if int(level) <= user_level or request.user.is_staff :
            question_details = question_data[0]
            return render(request, 'break_in/question.html', {'question_data':question_details, 'user_nick':user_nick, 'question_comments':question_comments})
        else:
            return render(request, 'base/error.html', {'error_code': 1, 'user_nick':user_nick}, status = 401)
    else:
        return render(request, 'base/error.html', {'error_code': 2, 'user_nick':user_nick}, status = 404)

@login_required
def submissions(request):
    user_submissions = Submission.objects.filter(submission_user__user_username=request.user.username).order_by('id')
    user_submissions = user_submissions.reverse()
    for sub in user_submissions:
        sub.submission_state = SUBMISSION_STATE_CHOICES[sub.submission_state]
    return render(request, 'break_in/submissions.html', {'user_submissions':user_submissions})

@csrf_protect
@login_required
def submit(request, level, id):
    context = RequestContext(request)
    user = User.objects.filter(user_username=request.user.username)[0]
    if int(user.user_access_level) < int(level):
        return render(request, 'base/error.html', {'error_code':1}, status = 401)
    #print request.method
    time_last = None
    time_last_query = Submission.objects.filter(submission_user__user_username=request.user.username).filter(submission_question__question_level=level).filter(submission_question__question_level_id=id).filter(submission_state='WA').order_by('submission_timestamp').last()
    if time_last_query:
        time_last = time_last_query.submission_timestamp
    time_limit = datetime.timedelta(0, 30)
    print time_last, datetime.datetime.now(utc)
    if(time_last is None or time_last + time_limit <= datetime.datetime.now(utc)):
        #ans_file = request.FILES.get("answer_file")
        #print ans_file, request.FILES
        ans_text = request.POST.get("answer_text")
        if ans_text is None:
            return HttpResponseRedirect('/contest/break_in/question/'+level+'/'+id)
        if ans_text and len(ans_text) > 255:
            # return HttpResponse(content = 'String too large.', status=413)
            return render(request, 'base/error.html', {'error_code':3} , status = 413)
        question = Question.objects.filter(question_level=level).filter(question_level_id=id)
        if len(question):
            question = question[0]
            submission = Submission(submission_question=question, submission_user=user, submission_string=ans_text)
            ans = submission.__check_ans__()
            level_subs = Submission.objects.filter(submission_user__user_username=request.user.username).filter(submission_question__question_level=level)
            level_acc_question_ids_query = level_subs.filter(submission_state='AC')       
            print level_subs, level_acc_question_ids_query
            level_acc_question_ids = set()
            for subs in level_acc_question_ids_query:
                level_acc_question_ids.add(subs.submission_question.question_level_id)
            print level_acc_question_ids
            if(ans == 'AC' and int(level) <= int(submission.submission_user.user_access_level) and int(id) not in level_acc_question_ids):
                print "Correct"
                #count = submission.submission_user.counter_inc(int(level))
                #if(count == 5):
                    #no_of_submissions = len(level_subs) + 1 #for current submission +1
                    #submission.submission_user.score_up(int(level)*20 - no_of_submissions)
                #if(count == 3):
                    #submission.submission_user.level_up()
                submission.submission_user.score_up(int(level)*100)
                submission.submission_user.save()
            submission.save()
    else:
        # return HttpResponse(content = 'Cannot submit before 30s of last submission.', status=403)
        return render(request, 'base/error.html', {'error_code':4}, status = 405)
    return HttpResponseRedirect('/contest/break_in/problems')

@csrf_protect
@login_required
def comment_submit(request, level, id):
    context = RequestContext(request)
    user = User.objects.filter(user_username=request.user.username)[0]
    if int(user.user_access_level) < int(level):
        return render(request, 'base/error.html', {'error_code':1}, status = 401)
    #print request.method
    time_last = None
    time_last_query = Comment.objects.filter(comment_user__user_username=request.user.username).order_by('comment_timestamp').last()
    if time_last_query:
        time_last = time_last_query.comment_timestamp
    time_limit = datetime.timedelta(0, 30)
    print time_last, datetime.datetime.now(utc)
    if(time_last is None or time_last + time_limit <= datetime.datetime.now(utc)):
        comment_text = request.POST.get("comment_text")
        if comment_text is None:
            return HttpResponseRedirect('/contest/break_in/question/'+level+'/'+id)
        if comment_text and len(comment_text) > 255:
            return render(request, 'base/error.html', {'error_code':3}, status = 411)
        question = Question.objects.filter(question_level=level).filter(question_level_id=id)
        if len(question):
            question = question[0]
            comment = Comment(comment_question=question, comment_user=user, comment_message=comment_text)
            comment.save()
    else:
        return render(request, 'base/error.html', {'error_code':5}, status = 405)
    return HttpResponseRedirect('/contest/break_in/question/'+level+'/'+id)


@login_required
def scoreboard(request):
    profile = User.objects.filter(user_username = request.user.username)[0]
    user_nick = profile.user_nick
    return render(request, 'break_in/scoreboard.html',  {'user_nick':user_nick})

@csrf_protect
@login_required
def register(request):
    context = RequestContext(request)
    profile = User.objects.filter(user_username = request.user.username)[0]
    user_nick = profile.user_nick
    user_team_check_query = TeamUser.objects.filter(teamuser_user__user_nick = profile.user_nick)
    if request.method == "GET" and len(user_team_check_query) == 0:
        return render(request, 'break_in/register.html', {'user_nick':user_nick})
    if len(user_team_check_query) != 0:
        user_team_check = user_team_check_query.first()
        get_team_object = user_team_check.teamuser_team
        teamuser_delete_query = TeamUser.objects.filter(teamuser_team = get_team_object)
        if request.method == "GET":
            teamuser_nicks = []
            for i in teamuser_delete_query:
                teamuser_nicks.append(i.teamuser_user.user_nick)
            return render(request, 'break_in/register.html', {'user_nick':user_nick, 'team_name':get_team_object.team_teamname,  'member_list':teamuser_nicks})
        for i in teamuser_delete_query:
            i.delete()
        team_delete_query = Team.objects.filter(team_teamname = get_team_object.team_teamname).first()
        team_delete_query.delete()
        return render(request, 'break_in/register.html', {'user_nick':user_nick}) 
    team_name = request.POST.get('user_team_name')
    team_member_nick = request.POST.get('user_team_member_nick')
    logger.debug(str(team_member_nick == ''))
    if team_name is None or team_member_nick is None:
        return render(request, 'break_in/register.html', {'user_nick':user_nick, 'error':10})
    if team_name == '':
        return render(request, 'break_in/register.html', {'user_nick':user_nick, 'error':10})
    team_object = Team(team_teamname=team_name)
    teamuser_object_1 = None
    teamuser_object_2 = None
    if team_member_nick != '':
        team_member_user = User.objects.filter(user_nick = team_member_nick)
        if len(team_member_user) == 0:
            return render(request, 'break_in/register.html', {'user_nick':user_nick, 'error':11})
        team_member_user = team_member_user[0]
    #try:
    #except IntegrityError:
        #return render(request, 'break_in/register.html', {'user_nick':user_nick, 'error':13})
    
    try:
        team_object.save()
        team_object = Team.objects.filter(team_teamname = team_name)[0]
        logger.debug(str(team_object)+str(team_object.id))
        logger.debug(str(teamuser_object_1))
        teamuser_object_1 = TeamUser(teamuser_team = team_object, teamuser_user = profile)
        teamuser_object_1.save()
        teamuser_object_1 = TeamUser.objects.filter(teamuser_user__user_nick = profile.user_nick)[0]
        logger.debug(str(teamuser_object_1))
        if team_member_nick != '':
            teamuser_object_2 = TeamUser(teamuser_team = team_object, teamuser_user = team_member_user)
            teamuser_object_2.save()
        logger.debug(str(teamuser_object_2))
    except IntegrityError as e:
        logger.debug('2 '+str(e))
        if team_object.id is not None:
            team_object.delete()
        if teamuser_object_1.id is not None:
            teamuser_object_1.delete()
        return render(request, 'break_in/register.html', {'user_nick':user_nick, 'error':13})
    return HttpResponseRedirect('/contest/break_in/register')   
