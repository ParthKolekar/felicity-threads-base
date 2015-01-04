from django.db import models
from django_countries.fields import CountryField
import datetime

def question_image_filepath(instance , filename):
	return '/'.join(['images' , instance.question_level , instance.question_level_id, filename])

def question_checker_script(instance , filename):
	return '/'.join(['checker' , instance.question_level , instance.question_level_id , filename])

def submission_storage_path(instance, filename):
	string = '/'.join(['submissions', instance.user.user_username, instance.question_level, instance.question_level_id, instance.id ]) 
	string += datetime.datetime.now().strftime("-%I:%M%p-%m-%d-%Y") 
	return string

# Create your models here.
class Question(models.Model):
	""" 
		This Database stores the questions that are to be rendered.
		Also provides descriptive functions which provide easy rendering abilities.
	"""	
	question_title = models.CharField(
		max_length = 255,
		unique = True
	)
	question_desc = models.TextField()
	question_image = models.ImageField(
		upload_to = question_image_filepath,
		#lambda instance, filename: '/'.join(['images' , instance.question_level , instance.question_level_id]), 
	)

	# Sets the question level and the identifier inside the level. 
	# Level can also be designated as question type.
	question_level = models.IntegerField()
	question_level_id = models.IntegerField()

	# question upload details.
	# Keep these fields in mind when you derive from base.
	FILE = "FL"
	STRING = "ST"
	UPLOAD_CHOICES = (
		( FILE , "File" ),
		( STRING , "String" ),
	)
	question_upload_type = models.CharField(
		max_length = 2, 
		choices = UPLOAD_CHOICES, 
		default = STRING
	)
	question_upload_file = models.FileField() # if upload_type == ST, ignore. 
	question_checker_script = models.FileField(
		upload_to = question_checker_script
		#lambda instance, filename: '/'.join(['checkers' , instance.question_level , instance.question_level_id]),
	)

class Team(models.Model):
	"""
		This database stores the Team Information.
	"""
	team_name = models.CharField(
		max_length = 255
	)
	team_score = models.IntegerField(
		default = 0
	)

class User(models.Model):
	"""
		This Database stores the User Information.
		The comments on the side refer to the 
		CAS login creds for reference.
	"""	
	user_username = models.CharField(
		max_length = 255
	) # returned by CAS::getUser(), normally equal to mail.
	user_email = models.EmailField(
		max_length=255,
		unique=True
	) #mail
	user_nick = models.CharField(
		max_length=255
	) # displayName
	user_firstname = models.CharField(
		max_length=255
	) # givenName
	user_surname = models.CharField(
		max_length=255
	) #sn
	user_country =  CountryField(
	)# c , ISO-alpha2
	user_location = models.CharField(
		max_length=255
	) #l

	user_last_ip = models.GenericIPAddressField(
		editable = False
	)
	user_timestamp = models.DateField(
		auto_now = True,
		auto_now_add = True
	)
	
	# This is the highest level of questions that one can access.
	user_access_level = models.IntegerField(
		default = 1,
		editable = False
	)
	
	#team attributes
	user_team = models.ForeignKey(Team)

class Submission(models.Model):
	"""
		This Database stores the Submissions Information.
	"""
	submission_question = models.ForeignKey(Question)
	submission_user = models.ForeignKey(User)
	submission_timestamp = models.DateField(
		auto_now = True,
		auto_now_add = True,
	)
	submission_storage = models.FileField(
		editable = False,
		upload_to = submission_storage_path,
	)
