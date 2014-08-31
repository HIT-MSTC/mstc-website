from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Dynamics(models.Model):
	title = models.CharField(max_length = 128)
	author = models.ForeignKey(User)
	publish_time = models.DateTimeField(auto_now = True)
	content = models.CharField(max_length = 5000)

	hasform = models.BooleanField(default = False)

	def __unicode__(self):
		return self.title

class Event(models.Model):
	name = models.CharField(max_length = 128)
	event_time = models.DateTimeField()
	number = models.IntegerField()
	now_num = models.IntegerField(default = 0)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	dynamics = models.OneToOneField(Dynamics)

	needname = models.BooleanField(default = False)
	needcollege = models.BooleanField(default = False)
	needgrade = models.BooleanField(default = False)
	needphone = models.BooleanField(default = False)
	needemail = models.BooleanField(default = False)
	needqq = models.BooleanField(default = False)
	needothername = models.BooleanField(default = False)
	othername = models.CharField(max_length = 16, default = 'Remark')

	def __unicode__(self):
		return self.name

class Tag(models.Model):
	title = models.CharField(max_length = 128)
	event = models.ForeignKey(Dynamics)

	def __unicode__(self):
		return self.title

class Partake(models.Model):
	name = models.CharField(max_length = 16)
	college = models.CharField(max_length = 32)
	grade = models.CharField(max_length = 4)
	phone = models.CharField(max_length = 11)
	email = models.EmailField(max_length = 75)
	qq = models.CharField(max_length = 12)
	other = models.CharField(max_length = 2048)
	event = models.ForeignKey(Event)

	def __unicode__(self):
		return self.name