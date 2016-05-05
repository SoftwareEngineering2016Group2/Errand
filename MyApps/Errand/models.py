#coding:utf-8
from __future__ import unicode_literals

from django.db import models

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
			return True;
		return False;
	def ChangePassword(self, newpassword):
		self.password = newpassword
		self.save()
		return True;
	def __unicode__(self):
		return self.username

class Userinfo(models.Model):
	nickname = models.CharField(max_length=16, default="John")
	def __unicode__(self):
		return self.nickname
