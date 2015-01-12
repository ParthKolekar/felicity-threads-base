from django.db import models
from base.models import Question as Q, Submission as S, User as U
# Create your models here.

class Question(Q):
    pass

class Submission(S):
    submission_question = models.ForeignKey(Question)
