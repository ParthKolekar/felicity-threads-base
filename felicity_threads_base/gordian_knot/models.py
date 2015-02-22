from django.db import models

from base.models import Comment as C
from base.models import Question as Q
from base.models import Submission as S
from base.models import User as U


# Create your models here.

class Question(Q):
    pass

class Submission(S):
    submission_question = models.ForeignKey(Question)


class Comment(C):
    comment_question = models.ForeignKey(Question)
