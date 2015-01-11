from django.db import models
from django_countries.fields import CountryField
import datetime

def question_image_filepath(instance , filename):
    return '/'.join(['images' , str(instance.question_level) , str(instance.question_level_id), filename])

def question_file_upload(instance, filename):
    return '/'.join(['question',str(instance.question_level), str(instance.question_level_id), filename])

def question_checker_upload(instance , filename):
    return '/'.join(['checker', str(instance.question_level), str(instance.question_level_id), filename])

def submission_storage_path(instance, filename):
    string = '/'.join(['submissions', instance.submission_user.user_username, str(instance.submission_question.question_level), str(instance.submission_question.question_level_id) ]) 
    string += '/'+datetime.datetime.now().strftime("%I:%M%p-%m-%d-%Y") 
    return string


FILE = "FL"
STRING = "ST"
UPLOAD_CHOICES = (
    ( FILE , "File" ),
    ( STRING , "String" ),
)

WA = 'WA'
AC = 'AC'
PR = 'PR'
SUBMISSION_STATE_CHOICES = (
    ( WA, "Wrong Answer" ),
    ( AC, "Accepted" ),
    ( PR, "Processing" ),
)

# Create your models here.
class Question(models.Model):

    """ 
        This Database stores the questions that are to be rendered.
        Also provides descriptive functions which provide easy rendering abilities.
    """
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.question_title)
    # Sets the question level and the identifier inside the level. 
    # Level can also be designated as question type.
    # Example - Question 4 of Level 3. 
    # ===> level = 4, level_id = 3
    question_level = models.IntegerField()
    question_level_id = models.IntegerField()

    # Question Details
    question_title = models.CharField(
        max_length = 255,
        unique = True,
    )
    question_desc = models.TextField()
    question_image = models.ImageField(
        blank = True,
        upload_to = question_image_filepath,
    )

    #TODO - Validate Question Fields based on Type.
    # However use is_question_valid till then.    

    # question upload details.
    # Keep these fields in mind when you derive from base.
    question_upload_type = models.CharField(
        max_length = 2, 
        choices = UPLOAD_CHOICES, 
        default = STRING,
    )
    
    # If ST then answer string is to be provided
    question_answer_string = models.CharField(
        blank = True,
        max_length = 255,
        default = '',
    )

    # If not ST then the upload file is the file to be compared to
    # and checker script is the one which checks the submission.
    question_upload_file = models.FileField(
        blank = True,
	upload_to = question_file_upload,
    ) # if upload_type == ST, ignore. 
    question_checker_script = models.FileField(
        blank = True,
        upload_to = question_checker_upload,
    )


    def is_question_accessible(self,level):
        if level >= self.question_level:
            return True
        return False

    def is_question_valid(self):
        if self.question_upload_type == STRING:
            return self.question_answer_string and True
        else:
            return self.question_upload_file and self.question_checker_script

    def check_submission(self,submission_string):
        if self.question_upload_type == STRING:
            return self.question_answer_string == submission_string
        else: #TODO -- FILE UPLOAD SUBMISSION CHECK
            # Essentially Something like this.
            # os.system ( "./" + self.question_checker_script + " " + self.upload_file + " " + self.submission_string )
            pass
            

"""class Team(models.Model):
    
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.team_name)

    team_name = models.CharField(
        max_length = 255,
    )
    team_score = models.IntegerField(
        editable = False,
        default = 0,
    )
"""

class User(models.Model):
    """
        This Database stores the User Information.
        The comments on the side refer to the 
        CAS login creds for reference.
    """ 

    def __str__(self):
        return str(self.user_username)

    user_username = models.CharField(
        max_length = 255,
    ) # returned by CAS::getUser(), normally equal to mail.
    user_email = models.EmailField(
        max_length=255,
        unique=True
    ) #mail
    user_nick = models.CharField(
        max_length=255,
    ) # displayName
    """user_country =  CountryField(
    ) # c , ISO-alpha2"""
    user_last_ip = models.GenericIPAddressField(
        editable = True,
    )
    user_timestamp = models.DateTimeField(
        auto_now = True,
        auto_now_add = True,
    )
    
    # This is the highest level of questions that one can access.
    user_access_level = models.IntegerField(
        default = 1,
        editable = False,
    )
    
    user_score = models.FloatField(
        default = 0,
        editable = False,
    )

    def level_up(self):
        self.user_access_level += 1

    def score_up(self, increment):
        self.user_score += increment
        
    """#team attributes
    user_team = models.ForeignKey(Team)
    
    def get_team_name(self):
        return self.user_team.team_name
    
    def get_team_score(self):
        return self.user_team.team_score
    """

class Submission(models.Model):
    """
        This Database stores the Submissions Information.
    """

    class Meta:
        abstract = True

    def __str__(self):
        return '_'.join([self.submission_question.question_title, self.submission_user.user_username])

    submission_user = models.ForeignKey(User)
    submission_timestamp = models.DateTimeField(
        auto_now = True,
        auto_now_add = True,
    )
    submission_string = models.CharField(
        editable = True,
        default = '',  
        max_length = 255,
    )
    submission_storage = models.FileField(
        editable = True,
        upload_to = submission_storage_path,
    )
    submission_state = models.CharField(
        max_length = 2,
        choices = SUBMISSION_STATE_CHOICES,
        default = PR,
    )
    submission_score = models.FloatField(
        default = 0,
    )

    def __check_ans__(self):
        if(self.submission_question.question_upload_type == FILE):
            pass
        elif(self.submission_question.check_submission(self.submission_string)):
            self.submission_state = AC
            self.submission_score = 100
        else:
            self.submission_state = WA
        return self.submission_state

    """def get_team_name(self):
        return self.submission_user.get_team_name()
    
    def get_team_score(self):
        return self.submission_user.get_team_score()
    """
