"""
    Module DocString
"""

import binascii
import datetime
import os

from django.db import models


def question_image_filepath(instance, filename):
    """
        Function DocString
    """
    return '/'.join(['images', str(instance.question_level), str(instance.question_level_id), binascii.b2a_hex(os.urandom(15)), filename])

def question_input_file_upload(instance, filename):
    """
        Function DocString
    """
    return '/'.join(['input', str(instance.question_level), str(instance.question_level_id), binascii.b2a_hex(os.urandom(15)), filename])

def question_gold_file_upload(instance, filename):
    """
        Function DocString
    """
    return '/'.join(['gold', str(instance.question_level), str(instance.question_level_id), binascii.b2a_hex(os.urandom(15)), filename])


def question_checker_upload(instance, filename):
    """
        Function DocString
    """
    return '/'.join(['checker', str(instance.question_level), str(instance.question_level_id), binascii.b2a_hex(os.urandom(15)), 'checker', filename])

def question_preprocess_upload(instance, filename):
    """
        Function DocString
    """
    return '/'.join(['checker', str(instance.question_level), str(instance.question_level_id), binascii.b2a_hex(os.urandom(15)), 'preprocess', filename])    

def submission_storage_path(instance, filename):
    """
        Function DocString
    """
    string = '/'.join(['submissions', instance.submission_user.user_nick, str(instance.submission_question.question_level), str(instance.submission_question.question_level_id)])
    string += '/'+datetime.datetime.now().strftime("%I:%M%p-%m-%d-%Y")
    string += filename
    return string


FILE = "FL"
STRING = "ST"
UPLOAD_CHOICES = (
    (FILE, "File"),
    (STRING, "String"),
)

WA = 'WA'
AC = 'AC'
PR = 'PR'
SUBMISSION_STATE_CHOICES = (
    (WA, "Wrong Answer"),
    (AC, "Accepted"),
    (PR, "Processing"),
)

class UTC(datetime.tzinfo):
    """
        Class DocString
    """
    def utcoffset(self, dt):
        """
            Function DocString
        """
        return datetime.timedelta(0)
    def tzname(self, dt):
        """
            Function DocString
        """
        return "UTC"
    def dst(self, dt):
        """
            Function DocString
        """
        return datetime.timedelta(0)

utc = UTC()

TIME_SINCE_MY_BIRTH = datetime.datetime(1995, 12, 21, 20, 5, 0, 0, utc)

# Create your models here.

class Language(models.Model):
    """
        Gives the Languages which can be compiled on the system for FILE type submissions.
    """

    def __str__(self):
        return str(self.language_name)

    language_compile_arguments = models.CharField(
        max_length = 255,
        blank = True,
        default = '',
        unique = False,
    )
    language_runtime_arguments = models.CharField(
        max_length = 255,
        blank = True,
        default = '',
        unique = False
    )
    language_file_extension = models.CharField(
        max_length = 16,
        blank = False,
        default = '',
        unique = True,
    )
    language_is_preprocessed = models.BooleanField(
        default = False,
    )
    language_is_sandboxed = models.BooleanField(
        default = False,
    )
    language_is_compiled = models.BooleanField(
        default = False,
    )
    language_is_checked = models.BooleanField(
        default = False,
    )
    language_is_executed = models.BooleanField(
        default = False,
    )
    language_name = models.CharField(
        max_length = 255,
        blank = False,
        default = '',
        unique = False,
    )


class Question(models.Model):
    """ 
        This Database stores the questions that are to be rendered.
        Also provides descriptive functions which provide easy rendering abilities.
    """

    class Meta:
        abstract = True

    def __str__(self):
        return " ".join([str(self.question_level), str(self.question_level_id) , str(self.question_title)])
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
        upload_to = question_input_file_upload,
    ) # if upload_type == ST, ignore.
    question_gold_upload_file = models.FileField(
        blank = True,
        upload_to = question_gold_file_upload,
    )
    question_checker_script = models.FileField(
        blank = True,
        upload_to = question_checker_upload,
    )
    question_preprocess_script = models.FileField(
        blank = True,
        upload_to = question_preprocess_upload,
    )
    question_restrict_language_to = models.ForeignKey(
            Language,
            blank=True,
            null=True,
            default=None,
        )
    # In Kilobytes and seconds
    question_time_limit = models.CharField(
       blank = True,
       max_length = 16,
       default = '',
    )
    question_memory_limit = models.CharField(
       blank = True,
       max_length = 16,
       default = '',
    )
    question_output_limit = models.CharField(
       blank = True,
       max_length = 16,
       default = '',
    )
    def is_question_accessible(self, level):
        """
            Function DocString
        """
        if level >= self.question_level:
            return True
        return False

    def is_question_valid(self):
        """
            Function DocString
        """
        if self.question_upload_type == STRING:
            return self.question_answer_string and True
        else:
            return self.question_upload_file and self.question_checker_script

    def check_submission(self, submission_string, submission_id):
        """
            Function DocString
        """
        if self.question_upload_type == STRING:
            return self.question_answer_string.lower().replace(' ', '') == submission_string.lower().replace(' ', '')
        else:
            raise Exception("Question not String Type.")

class User(models.Model):
    """
        This Database stores the User Information.
        The comments on the side refer to the
        CAS login creds for reference.
    """

    def __str__(self):
        return "    ".join([str(self.user_nick), str(self.user_username)])

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
    user_last_ip = models.GenericIPAddressField(
        editable = True,
        default = '0.0.0.0',
    )

    # This is the highest level of questions that one can access.
    user_access_level = models.IntegerField(
        default = 1,
        editable = True,
    )
   
    user_score = models.FloatField(
        default = 0,
        editable = True,
    )

    def level_up(self):
        """
           Increments User level. Call with care.
        """
        self.user_access_level += 1

    def score_up(self, increment_by):
        """
           Score Up by parameter increment_by
        """
        self.user_score += increment_by

    def counter_inc(self, level):
        """
            Cheap hack to increment user_access level states.
        """

        if level == 1:
            self.user_level_1 += 1
            return self.user_level_1
        elif level == 2:
            self.user_level_2 += 1
            return self.user_level_2
        elif level == 3:
            self.user_level_3 += 1
            return self.user_level_3
        elif level == 4:
            self.user_level_4 += 1
            return self.user_level_4
        elif level == 5:
            self.user_level_5 += 1
            return self.user_level_5
        elif level == 6:
            self.user_level_6 += 1
            return self.user_level_6
        elif level == 7:
            self.user_level_7 += 1
            return self.user_level_7
        elif level == 8:
            self.user_level_8 += 1
            return self.user_level_8
        elif level == 9:
            self.user_level_9 += 1
            return self.user_level_9
        elif level == 10:
            self.user_level_10 += 1
            return self.user_level_10
        elif level == 11:
            self.user_level_11 += 1
            return self.user_level_11
        elif level == 12:
            self.user_level_12 += 1
            return self.user_level_12
        elif level == 13:
            self.user_level_13 += 1
            return self.user_level_13
        elif level == 14:
            self.user_level_14 += 1
            return self.user_level_14
        elif level == 15:
            self.user_level_15 += 1
            return self.user_level_15
        elif level == 16:
            self.user_level_16 += 1
            return self.user_level_16
        elif level == 17:
            self.user_level_17 += 1
            return self.user_level_17
        elif level == 18:
            self.user_level_18 += 1
            return self.user_level_18
        elif level == 19:
            self.user_level_19 += 1
            return self.user_level_19
        elif level == 20:
            self.user_level_20 += 1
            return self.user_level_20
        elif level == 21:
            self.user_level_21 += 1
            return self.user_level_21
        elif level == 22:
            self.user_level_22 += 1
            return self.user_level_22
        elif level == 23:
            self.user_level_23 += 1
            return self.user_level_23
        elif level == 24:
            self.user_level_24 += 1
            return self.user_level_24
        elif level == 25:
            self.user_level_25 += 1
            return self.user_level_25
        elif level == 26:
            self.user_level_26 += 1
            return self.user_level_26
        elif level == 27:
            self.user_level_27 += 1
            return self.user_level_27
        elif level == 28:
            self.user_level_28 += 1
            return self.user_level_28
        elif level == 29:
            self.user_level_29 += 1
            return self.user_level_29
        elif level == 30:
            self.user_level_30 += 1
            return self.user_level_30

    # flash message
    user_notification_flash = models.BooleanField(
        default = False,
    )

    user_level_1 = models.IntegerField(
        default = 0,
    )

    user_level_2 = models.IntegerField(
        default = 0,
    )

    user_level_3 = models.IntegerField(
        default = 0,
    )

    user_level_4 = models.IntegerField(
        default = 0,
    )

    user_level_5 = models.IntegerField(
        default = 0,
    )

    user_level_6 = models.IntegerField(
        default = 0,
    )

    user_level_7 = models.IntegerField(
        default = 0,
    )

    user_level_8 = models.IntegerField(
        default = 0,
    )

    user_level_9 = models.IntegerField(
        default = 0,
    )

    user_level_10 = models.IntegerField(
        default = 0,
    
        )
    user_level_11 = models.IntegerField(
        default = 0,
    )

    user_level_12 = models.IntegerField(
        default = 0,
    )

    user_level_13 = models.IntegerField(
        default = 0,
    )

    user_level_14 = models.IntegerField(
        default = 0,
    )

    user_level_15 = models.IntegerField(
        default = 0,
    )

    user_level_16 = models.IntegerField(
        default = 0,
    )

    user_level_17 = models.IntegerField(
        default = 0,
    )

    user_level_18 = models.IntegerField(
        default = 0,
    )

    user_level_19 = models.IntegerField(
        default = 0,
    )

    user_level_20 = models.IntegerField(
        default = 0,
    )

    user_level_21 = models.IntegerField(
        default = 0,
    )

    user_level_22 = models.IntegerField(
        default = 0,
    )

    user_level_23 = models.IntegerField(
        default = 0,
    )

    user_level_24 = models.IntegerField(
        default = 0,
    )

    user_level_25 = models.IntegerField(
        default = 0,
    )

    user_level_26 = models.IntegerField(
        default = 0,
    )

    user_level_27 = models.IntegerField(
        default = 0,
    )

    user_level_28 = models.IntegerField(
        default = 0,
    )

    user_level_29 = models.IntegerField(
        default = 0,
    )

    user_level_30 = models.IntegerField(
        default = 0,
    )


class Submission(models.Model):
    """
        This Database stores the Submissions Information.
    """

    class Meta:
        abstract = True

    def __str__(self):
        return "    ".join([str(self.submission_score), str(self.submission_question.question_title), str(self.submission_user.user_nick)])

    submission_user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related")

    submission_timestamp = models.DateTimeField(
        auto_now = True,
        auto_now_add = True,
    )
    submission_string = models.CharField(
        blank = True,
        editable = True,
        default = '',  
        max_length = 255,
    )
    submission_storage = models.FileField(
        editable = True,
        upload_to = submission_storage_path,
        blank = True,
    )
    submission_state = models.CharField(
        max_length = 2,
        choices = SUBMISSION_STATE_CHOICES,
        default = PR,
    )
    submission_score = models.FloatField(
        default = 0,
    )

    submission_runtime_log = models.CharField(
        max_length = 255,
        default = "",
        blank = True,
    )

    def __check_ans__(self):
        if(self.submission_question.question_upload_type == FILE):
            raise Exception("Wrong Method Called.Question not String Type.")
        elif self.submission_question.check_submission(self.submission_string,self.id):
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

class ClarificationMessages(models.Model):
    """
        Clarification Messages to display on Index Page.
    """

    def __str__(self):
        return str(self.clarification_messages_message)

    clarification_messages_message = models.CharField(
        max_length = 255,
    )

class Comment(models.Model):
    """
        Comments of user. Needs approval from admins.
    """

    class Meta:
        abstract = True

    def __str__(self):
        return "    ".join([str(self.comment_is_approved), str(self.comment_user.user_nick), str(self.comment_message)])

    comment_timestamp = models.DateTimeField(
        auto_now = True,
        auto_now_add = True,
    )

    comment_message = models.CharField(
        max_length = 255,
        default = '',
    )

    comment_user = models.ForeignKey(User)

    comment_is_approved = models.BooleanField(
        default = False,
    )
