from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Dynamics(models.Model):
	title = models.CharField(max_length = 128)
	author = models.ForeignKey(User)
	publish_time = models.DateTimeField(auto_now = True)
	content = models.CharField(max_length = 5000)

	def __unicode__(self):
		return self.title

class Event(models.Model):
	name = models.CharField(max_length = 128)
	event_time = models.DateTimeField()
	number = models.IntegerField()
	now_num = models.IntegerField()
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	dynamics = models.OneToOneField(Dynamics)

	def __unicode__(self):
		return self.name

class Tag(models.Model):
	title = models.CharField(max_length = 128)
	event = models.ForeignKey(Event)

	def __unicode__(self):
		return self.title

class Partake(models.Model):
	name = models.CharField(max_length = 16)
	stu_id = models.CharField(max_length = 10)
	college = models.CharField(max_length = 32)
	sex = models.BooleanField()
	phone = models.CharField(max_length = 11)
	email = models.EmailField(max_length = 75)
	qq = models.CharField(max_length = 12)
	event = models.ForeignKey(Event)

	def __unicode__(self):
		return self.name