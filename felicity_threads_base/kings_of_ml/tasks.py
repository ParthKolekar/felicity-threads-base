from __future__ import absolute_import

from celery import task,shared_task
from felicity_threads_base.celery import app
from felicity_threads_base.settings import MEDIA_ROOT

from kings_of_ml.models import Question, Submission
from base.models import User

import imp
import os.path

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@app.task()
def checker_queue(submission_id, bool_level_up):
    submission = Submission.objects.filter(id=submission_id)[0]
    # the slicing of 15 to remove /contest/media.
    # Yeah. I'm lazy that way.
    checker_path = submission.submission_question.question_checker_script.path
    checker_path = os.path.join(MEDIA_ROOT, checker_path)

    module = imp.load_source('kings_of_ml.checker', checker_path)
    level = submission.submission_question.question_level
    level_subs = Submission.objects.filter(submission_user__user_username=submission.submission_user.user_username).filter(submission_question__question_level=level)  

    # the slicing of 15 to remove /contest/media.
    # Yeah. I'm lazy that way.
    # Comments also copied at times. So. That.
    perfect_file_path = submission.submission_question.question_upload_file.path
    to_check_file_path = submission.submission_storage.path

    # the checker script must 'thus' contain a function check(perfect_file_path,to_check_file_path) 
    # and should return a value between 0 to 100.
    score = module.check(perfect_file_path, to_check_file_path)
    
    # the level up and the 'AC', 'WA' rules here.
    if score > 0:
        submission.submission_state = 'AC'
        submission.submission_score = score
        if score == 100 and bool_level_up:
            count = submission.submission_user.counter_inc(int(level))
            if(count == 5):
                no_of_submissions = len(level_subs) + 1 #for current submission +1
                submission.submission_user.score_up(int(level)*20 - no_of_submissions)
            if(count == 3):
                submission.submission_user.level_up()
            submission.submission_user.score_up(int(level)*100)
            submission.submission_user.save()
    else:
        submission.submission_state = 'WA'
    submission.save()
    return str(submission) + " " + str(score)
