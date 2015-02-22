from __future__ import absolute_import

import commands
import datetime
import imp
import os

from celery import shared_task, task

from base.models import Language, User
from code_da_circuit.models import Question, Submission
from felicity_threads_base.celery import app
from felicity_threads_base.settings import MEDIA_ROOT


@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@app.task()
def checker_queue(submission_id, bool_level_up):
    submission = Submission.objects.filter(id=submission_id)[0]
    checker_path = submission.submission_question.question_checker_script.path
    preprocessor_path = submission.submission_question.question_preprocess_script.path
    try:
       checker_module = imp.load_source('code_da_circuit.checker', checker_path)
    except:
        checker_module = None
    try:
        preprocessor_module = imp.load_source('code_da_circuit.preprocessor',preprocessor_path)
    except:
        preprocessor_module = None
    language = submission.submission_question.question_restrict_language_to
    # The file paths are fetched here.
    try:
        input_file_path = submission.submission_question.question_upload_file.path
    except:
        input_file_path = "/dev/null"
    try:
        gold_file_path = submission.submission_question.question_gold_upload_file.path
    except:
        gold_file_path = "/dev/null"
    # This can be a code (to compile or interpret) 
    # or a file to just diff
    try:
        submission_file_path = submission.submission_storage.path
        submission_base_dir = "/".join(submission.submission_storage.path.split("/")[:-1])
        if not submission_file_path:
            return
    except:
        return 
    # The Preprocessing happens here.
    if language.language_is_preprocessed:
        pre_passed = preprocessor_module.check(submission_file_path)
    else:
        pre_passed = True
    #this is where we compile the code.
    correct_compiled = True
    executable = submission_base_dir + str(submission.id) + '.executable' 
    if language.language_is_compiled and pre_passed:
        compile_status, compile_output = commands.getstatusoutput(language.language_compile_arguments % (executable, submission_file_path) ) 
        #if compiled, executable is the executable file.
        if compile_status != 0:
            correct_compiled = False
            submission.submission_runtime_log = compile_output
        else:
            submission.submission_runtime_log = "Compiled: OK "
    elif (not language.language_is_compiled) and pre_passed:
        executable = submission_file_path # If the thing is not compiled, excutable is the file to be interpreted.
    #this is where we execute/interpret the code.
    correct_executed = True
    output_file_path = submission_base_dir + str(submission.id) + ".output"
    if language.language_is_executed and pre_passed and correct_compiled:
        if language.language_is_sandboxed:
            exec_status, exec_output = commands.getstatusoutput( language.language_runtime_arguments % (input_file_path, output_file_path, executable, submission.submission_question.question_time_limit, submission.submission_question.question_memory_limit, submission.submission_question.question_output_limit ) ) 
        else:
            exec_status, exec_output = commands.getstatusoutput( language.language_runtime_arguments % (executable , input_file_path, output_file_path ) ) #Changed it to default again.
        if exec_status != 0:
             correct_executed = False
             submission.submission_runtime_log = exec_output
        else:
             submission.submission_runtime_log = "Runtime: OK "
    question_base_dir = "".join(submission.submission_question.question_checker_script.path.split("/")[:-1])
    # this is where we diff/check the code as per checker script but not always. ( :/ )
    # the checker script must 'thus' contain a function check(args)
    # and should return a value between 0 to 100.
    if language.language_is_checked and pre_passed and correct_compiled and correct_executed:
        try:
            score = checker_module.check(input_file_path, gold_file_path, submission_file_path, output_file_path, executable, question_base_dir)
        except:
            score = -2.0
    else:
        score = -1.0
    # the level up and the 'AC', 'WA' rules here 
    level = submission.submission_question.question_level
    level_subs = Submission.objects.filter(submission_user__user_username=submission.submission_user.user_username).filter(submission_question__question_level=level)  
    if score > 0:
        submission.submission_state = 'AC'
        submission.submission_score = score
                count = submission.submission_user.counter_inc(int(level))
                if(count == 1):
                    submission.submission_user.level_up()
                    submission.submission_user.score_up(score)
                submission.submission_user.save()
    else:
        submission.submission_state = 'WA'
        submission.submission_score = 0.0 # Wrong Answer means 0.0 I get score as -1.0
    if not submission.submission_runtime_log:
        submission.submission_runtime_log = "Nothing to Report"
    submission.save()
    try:
        os.remove(output_file_path)
    except:
        pass
    return str(submission) + " " + str(score)
