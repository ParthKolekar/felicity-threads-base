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
    
    def __str__(self):
        return str(self.team_teamname)
    
    team_teamname = models.CharField(
            default='',
            max_length = 255,
            unique = True,
    )

class TeamUser(models.Model):
    
    def __str__(self):
        return str(self.teamuser_team.team_teamname) + '_' + str(self.teamuser_user.user_nick)

    teamuser_team = models.ForeignKey(Team)
    teamuser_user = models.ForeignKey(U, unique=True)
