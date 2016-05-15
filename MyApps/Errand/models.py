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
	def ToJSON(self):
		return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]), default=default)

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
	def ToJSON(self):
		return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]), default=default)


