from __future__ import absolute_import

import imp
import os.path

from celery import shared_task, task

from base.models import User
from felicity_threads_base.celery import app
from felicity_threads_base.settings import MEDIA_ROOT
from kings_of_ml.models import Question, Submission


@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@app.task()
def checker_queue(submission_id, bool_level_up):
    submission = Submission.objects.filter(id=submission_id)[0]
    checker_path = submission.submission_question.question_checker_script.path
    module = imp.load_source('kings_of_ml.checker', checker_path)
    
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
