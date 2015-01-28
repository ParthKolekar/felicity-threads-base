from __future__ import absolute_import

from celery import task,shared_task
from felicity_threads_base.celery import app

from kings_of_ml.models import Question, Submission
from base.models import User

import importlib

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@app.task()
def checker_queue(submission_id, bool_level_up):
    
    submission = Submission.objects.filter(id=submission_id)[0]
    
    module = importlib.import_module(submission.submission_question.question_checker_script, package=None)

    level = submission.submission_question.question_level
    level_subs = Submission.objects.filter(submission_user__user_username=submission.submission_user.user_username).filter(submission_question__question_level=level)        
    
    # the checker script must thus contain a function check(perfect_file,to_check_file) 
    # and should return a value between 0 to 100.
    score = module.check(submission.submission_question.question_upload_file, submission.submission_storage)

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
                
    return str(submission)+"  Score: "+ score
