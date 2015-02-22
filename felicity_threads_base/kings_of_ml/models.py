import datetime

from django.db import models

from base.models import Comment as C
from base.models import Question as Q
from base.models import Submission as S
from base.models import User as U


# Create your models here.

def submission_code_storage_path(instance, filename):
    string = '/'.join(['submissions', 'codes' , instance.submission_user.user_nick, str(instance.submission_question.question_level), str(instance.submission_question.question_level_id) ]) 
    string += '/'+datetime.datetime.now().strftime("%I:%M%p-%m-%d-%Y") 
    return string

class Question(Q):
    pass

class Submission(S):
    submission_question = models.ForeignKey(Question)
    submission_code = models.FileField(
        upload_to = submission_code_storage_path,
        blank = True,
    )

class Comment(C):
    comment_question = models.ForeignKey(Question)
