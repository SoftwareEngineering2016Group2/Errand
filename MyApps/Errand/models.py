#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime
import json



class Account(models.Model):
	username = models.CharField(max_length=10, primary_key=True)
	password = models.CharField(max_length=16)
	activecode = models.CharField(max_length=4)
	active = models.BooleanField(default=False)
	userinfo = models.OneToOneField('Userinfo', related_name='account')
	#something strange??
	taskRelated = models.OneToOneField('TaskRelated',related_name='account')
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
	birthday = models.DateField(default='1900-1-1')
	signature = models.CharField(max_length=128, blank=True, default="")
	head_photo = models.ImageField(upload_to='head_pic', default='head_pic/default.jpeg')
	def ChangeUserinfo(self, data):
		self.nickname = data['nickname']
		self.sex = data['sex']
		self.phone_number = data['phone_number']
		self.birthday = data['birthday']
		self.signature = data['signature']
		self.save()
		return True

	def ChangeAvatar(self, avatar):
		if self.avatar.name != 'defaul.jpg':
			self.avatar.delete(False)
		self.avatar = avatar
		self.save()
		return True



	def __unicode__(self):
		return self.nickname


class TaskRelated(models.Model):
	taskCompleted = models.IntegerField(default=0)
	taskCreated = models.IntegerField(default=0)
	scores = models.IntegerField(default=0)

	def updateTaskCompleted(self, add=1):
		self.taskCompleted += add
		self.save()
		return True

	def updateTaskCreated(self,add=1):
		self.taskCreated += add
		self.save()
		return True

	def updateScores(self,score):
		self.scores += score
		self.save()
		return True

class Task(models.Model):
	create_account = models.ForeignKey('Account', related_name='created_account', on_delete=models.CASCADE)
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
	response_accounts = models.ManyToManyField('Account', related_name='response_accounts')
	execute_account = models.ForeignKey('Account', null=True, related_name='execute_account', on_delete=models.CASCADE)
	#task_actions = models.ManyToManyField(TaskAction)
	reward = models.CharField(max_length=16, default='1 RMB')
	comment = models.CharField(max_length=128, default='No Comment')
	score = models.IntegerField(default=-1)
	def IsCreator(self, username):
		return self.create_account.username == username
	def InWaiting(self):
		return self.status == 'W'
	def InAccpted(self):
		return self.status == 'A'
	def InClosed(self):
		return self.status == 'C'
	def CanChange(self, username):
		return self.IsCreator(username) and self.InWaiting()
	def CanSelect(self, username):
		return self.IsCreator(username) and self.InWaiting()
	def CanClose(self, username):
		return self.IsCreator(username) and (self.InAccpted() or self.InClosed())
	def CanComment(self, username):
		return self.IsCreator(username) and self.InClosed()
	def ChangeTask(self, data):
		self.headline = data['headline']
		self.detail = data['detail']
		self.reward = data['reward']
		self.save()
	def Accept(self, account):
		self.status = 'A'
		self.execute_account = account
		self.save()
	def Close(self):
		self.status = 'C'
		self.save()
	def Comment(self, data):
		self.comment = data['comment']
		self.score = data['score']
		self.save()
	def getScore(self):
		return self.score
	def scoreDefault(self):
		return self.score == -1



class TaskAction(models.Model):
	start_time = models.DateTimeField(default=None)
	end_time = models.DateTimeField(default=None)
	place = models.CharField(max_length=16, default="classroom")
	action = models.CharField(max_length=50, default="do something")
	task_belong = models.ForeignKey('Task', related_name='task_actions', on_delete=models.CASCADE)
	def ChangeTaskAction(self, data):
		self.start_time = data['start_time']
		self.end_time = data['end_time']
		self.place = data['place']
		self.action = data['action']
		self.save()
		return True


