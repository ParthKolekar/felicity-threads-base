from __future__ import absolute_import

from celery import task,shared_task
from felicity_threads_base.celery import app
from felicity_threads_base.settings import MEDIA_ROOT
from tle.models import Question, Submission
from base.models import User
import imp
import os.path
import commands

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@app.task()
def checker_queue(submission_id, bool_level_up):
    submission = Submission.objects.filter(id=submission_id)[0]
    checker_path = submission.submission_question.question_checker_script.path
    module = imp.load_source('tle.checker', checker_path)
    file_extension = submission.submission_storage.path


    return str(file_extension.split('/')[:-1])

    status, output = commands.getstatusoutput(';') 
    
    level = submission.submission_question.question_level
    level_subs = Submission.objects.filter(submission_user__user_username=submission.submission_user.user_username).filter(submission_question__question_level=level)  

    perfect_file_path = submission.submission_question.question_upload_file.path
    to_check_file_path = submission.submission_storage.path

    # the checker script must 'thus' contain a function check(perfect_file_path,to_check_file_path) 
    # and should return a value between 0 to 100.
    try:
        score = module.check(perfect_file_path, to_check_file_path)
    except:
        score = -1.0

    # the level up and the 'AC', 'WA' rules here.
    if score > 0:
        submission.submission_state = 'AC'
        submission.submission_score = score
    else:
        submission.submission_state = 'WA'
        submission.submission_score = 0.0 # Wrong Answer means 0.0 I get score as -1.0
    submission.save()
    return str(submission) + " " + str(score)
