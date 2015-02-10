from django.db import models
from base.models import Question as Q, Submission as S, Comment as C, User as U
import datetime
# Create your models here.

class Question(Q):
    pass

class Submission(S):
    submission_question = models.ForeignKey(Question)

class Comment(C):
    comment_question = models.ForeignKey(Question)
