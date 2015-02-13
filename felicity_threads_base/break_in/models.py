from django.db import models
from base.models import Question as Q, Submission as S, Comment as C, User as U
# Create your models here.

class Question(Q):
    pass

class Submission(S):
    submission_question = models.ForeignKey(Question)


class Comment(C):
    comment_question = models.ForeignKey(Question)

class Team(models.Model):
    team_user_first = models.ForeignKey(U, related_name='User1')
    team_user_second = models.ForeignKey(U, blank=True, related_name='User2')
    team_name = models.CharField(
            default='',
            max_length = 255,
    )

