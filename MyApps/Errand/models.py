#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime
#from bson import json_util
import json
def default(o):
	if type(o) is datetime.date or type(o) is datetime.datetime:
		return o.isoformat()
	#if type(o) is decimal.Decimal:
		#return float(o)


class Account(models.Model):
	username = models.CharField(max_length=16, primary_key=True)
	password = models.CharField(max_length=16)
	activecode = models.CharField(max_length=4)
	active = models.BooleanField(default=False)
	userinfo = models.ForeignKey('Userinfo', related_name='account')
	def Active(self, num):
		if num == self.activecode:
			self.active = True
			self.save()
			return True
		return False
	def ChangePassword(self, newpassword):
		self.password = newpassword
		self.save()
		return True;
	def __unicode__(self):
		return self.username

class Userinfo(models.Model):
	MALE = 'M'
	FEMALE = 'F'
	SEX_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	nickname = models.CharField(max_length=16, default="John")
	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)
	phone_number = models.CharField(max_length=11, default="13000000000")
	birthday = models.DateField(default=timezone.now().date())
	signature = models.CharField(max_length=140, blank=True, default="")

	def ChangeUserinfo(self, data):
		self.nickname = data['nickname']
		self.sex = data['sex']
		self.phone_number = data['phone_number']
		self.birthday = data['birthday']
		self.signature = data['signature']
		self.save()
		return True

	def __unicode__(self):
		return self.nickname
	

class Task(models.Model):
	create_account = models.ForeignKey('Account', related_name='created_account')
	create_time = models.DateTimeField(default=None)
	WAITING = 'W'
	ACCEPTED = 'A'
	CLOSED = 'C'
	STATUS_CHOICES = (
		(WAITING, 'Waiting'),
		(ACCEPTED, 'Accepted'),
		(CLOSED, 'Closed'),
	)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=WAITING)
	headline = models.CharField(max_length=16, default='New Task')
	detail = models.CharField(max_length=128, default='New Task')
	response_accounts = models.ManyToManyField(Account)
	execute_accounts = models.ForeignKey('Account', null=True, related_name='execute_account')
	#task_actions = models.ManyToManyField(TaskAction)
	reward = models.CharField(max_length=16, default='1 RMB')

class TaskAction(models.Model):
	start_time = models.DateTimeField(default=None)
	end_time = models.DateTimeField(default=None)
	place = models.CharField(max_length=16, default="classroom")
	action = models.CharField(max_length=50, default="do something")
	task_belong = models.ForeignKey('Task', related_name='task_actions')
	def ChangeTaskAction(self, data):
		self.start_time = data['start_time']
		self.end_time = data['end_time']
		self.place = data['place']
		self.action = data['action']
		self.save()
		return True

