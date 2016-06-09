#!/usr/bin/python
# -*-coding:UTF-8 -*-
from django.test import TestCase, Client
import random
import datetime

import urllib
import http.cookiejar as cookielib
from django.core.serializers import serialize,deserialize
from .models import Account, Userinfo, Task, TaskAction, TaskRelated
import json
import simplejson
import sys


cj = cookielib.CookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

HEADER = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
	'Referer' : 'http://202.206.1.163/logout.do'
}

url = 'http://127.0.0.1:8000/Errand/'
#url = 'http://139.129.47.180:8002/Errand/'

def geturlopen(hosturl, postdata = {}, headers = HEADER):
	enpostdata = urllib.parse.urlencode(postdata).encode('utf-8') 
	urlrequest = urllib.request.Request(hosturl, enpostdata, headers)
	urlresponse = urllib.request.urlopen(urlrequest)
	return urlresponse


def getData(uri, data = {}):
	return geturlopen(url + uri, data).read().decode('utf-8')

import threading

P = 20
N = 250

class ConcurrenceTestCase(TestCase):
	cnt_success = 0
	cnt_fail = 0
	clients = []
	username = []
	tasks_pk = []
	taskactions_pk = []
	thread_username = []
	def Print(self, opt):
		res = '\r%21s : %5d %5d %7.3f %7.3fms'% (opt, self.cnt_success, self.cnt_fail, self.cnt_success / (self.cnt_success + self.cnt_fail), self.total_time / 1000 /self.cnt_success)
		sys.stdout.write(res)
		sys.stdout.flush()
	def Register(self, c, tid):
		flag = False
		while (flag == False):
			try:
				flag = True
				response = c.get('/Errand/')
			except Exception as err:
				flag = False

		for i in range(N):
			username = self.username[random.randint(0, N * P - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/register', {'username': username, 'password': '123'})		
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('Register')

	def Active(self, c, tid):
		for i in range(N):
			username = self.username[random.randint(0, N * P - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/active', {'username': username, 'password': '123', 'activecode': '1111'})		
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				
				else:
					self.cnt_fail += 1
				self.Print('Active')

	def LogIn(self, c, tid):
		for i in range(N):
			username = self.username[random.randint(0, N * P - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/login', {'username': username, 'password': '123'})		
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('LogIn')

	def LogOut(self, c, tid):
		for i in range(N):
			try:
				starttime = datetime.datetime.now()
				response = c.get('/Errand/logout')
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('LogOut')

	def ChangePassword(self, c, tid):
		for i in range(N):
			username = self.username[random.randint(0, N * P - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/changepassword', {'username': username, 'password': '123', 'newpassword': '123'})		
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('ChangePassword')

	def ChangeUserinfo(self, c, tid):
		flag = False
		while (flag == False):
			try:
				username = self.username[random.randint(0, N * P - 1)]
				response = c.post('/Errand/login', {'username': username, 'password': '123'})
				if (response.status_code == 200 and str(response.content.decode('utf-8')) == 'OK'):
					flag = True
					self.thread_username[tid] = username
			except Exception as err:
				flag = False

		for i in range(N):
			username = self.username[random.randint(0, N * P - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/changeuserinfo', {'nickname':'Sun', 'sex' :'M', 'phone_number':'13888888888', 'birthday':'1994-10-11', 'signature':'Sleeping..'})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('ChangeUserinfo')

	def AddTask(self, c, tid):
		for i in range(N):
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/addtask', {'headline':'取快递', 'detail':'取快递', 'reward':'鸡腿饭'})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					task = simplejson.loads(response.content.decode('utf-8'))[0]
					self.tasks_pk.append(task['pk'])
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('AddTask')

	def ChangeTask(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			pk = self.tasks_pk[random.randint(0, l - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/changetask', {'pk': pk, 'headline':'取快递', 'detail':'取快递', 'reward':'鸡腿饭'})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('ChangeTask')

	def AddTaskAction(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			pk = self.tasks_pk[random.randint(0, l - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/addtaskaction', {'pk': pk, 'start_time' : '2011-10-11 12:00:00', 'end_time' : '2011-10-11 13:00:00', 'place' : 'er jiao', 'action' : 'gei wo'})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					if (str(response.content.decode('utf-8')) != 'FAILED : You can\'t change the task.'):
						taskaction = simplejson.loads(response.content.decode('utf-8'))[0]
						self.taskactions_pk.append(taskaction['pk'])
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('AddTaskAction')
	def ChangeTaskAction(self, c, tid):
		l = len(self.taskactions_pk)
		for i in range(N):
			pk = self.taskactions_pk[random.randint(0, l - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/changetaskaction', {'pk': pk, 'start_time' : '2011-10-11 12:00:00', 'end_time' : '2011-10-11 13:00:00', 'place' : 'er jiao', 'action' : 'gei wo'})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('ChangeTaskAction')
	def RemoveTaskAction(self, c, tid):
		l = len(self.taskactions_pk)
		for i in range(N):
			pk = self.taskactions_pk[random.randint(0, l - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/removetaskaction', {'pk': pk})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('RemoveTaskAction')

	def RemoveTask(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			pk = self.tasks_pk[random.randint(0, l - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/removetask', {'pk': pk})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('RemoveTask')

	def ResponseTask(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			#pk = self.tasks_pk[random.randint(0, l - 1)]
			pk = i
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/responsetask', {'pk': pk})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('ResponseTask')

	def SelectTaskExecutor(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			#pk = self.tasks_pk[random.randint(0, l - 1)]
			pk = i
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/selecttaskexecutor', {'username': self.thread_username[tid], 'pk': pk})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('SelectTaskExecutor')

	def CloseTask(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			pk = self.tasks_pk[random.randint(0, l - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/closetask', {'pk': pk})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('CloseTask')

	def CommentTask(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			pk = self.tasks_pk[random.randint(0, l - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/commenttask', {'pk': pk, 'score': 5, 'comment': 'Very Good'})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('CommentTask')

	def BrowseAllTask(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			#pk = self.tasks_pk[random.randint(0, l - 1)]
			pk = i
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/browsealltask', {'pk': pk})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('BrowseAllTask')
	def SeeTask(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			#pk = self.tasks_pk[random.randint(0, l - 1)]
			pk = i
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/seetask', {'pk': pk})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('SeeTask')

	def SearchTask(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			#pk = self.tasks_pk[random.randint(0, l - 1)]
			pk = i
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/searchtask', {'pk': pk, 'text': 'er jiao'})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('SearchTask')
	def GetTaskActions(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			pk = self.tasks_pk[random.randint(0, l - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/gettaskactions', {'pk': pk})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('GetTaskActions')

	def OrderByTaskCompleted(self, c, tid):
		for i in range(N):
			try:
				starttime = datetime.datetime.now()
				response = c.get('/Errand/orderbytaskcompleted')
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('OrderByTaskCompleted')

	def OrderByTaskCreated(self, c, tid):
		for i in range(N):
			try:
				starttime = datetime.datetime.now()
				response = c.get('/Errand/orderbytaskcreated')
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('OrderByTaskCreated')

	def OrderByScores(self, c, tid):
		for i in range(N):
			try:
				starttime = datetime.datetime.now()
				response = c.get('/Errand/orderbyscores')
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('OrderByScores')

	def GetUserTask(self, c, tid):
		l = len(self.tasks_pk)
		for i in range(N):
			pk = self.tasks_pk[random.randint(0, l - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/getusertask', {'pk': pk, 'typeOfTask': 'execute_account', 'state': 'W', 'username': self.thread_username[tid]})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('GetUserTask')

	def GetUserProfile(self, c, tid):
		for i in range(N):
			username = self.username[random.randint(0, N * P - 1)]
			try:
				starttime = datetime.datetime.now()
				response = c.post('/Errand/getuserprofile', {'username': username})
			except Exception as err:
				self.cnt_fail += 1
			else:
				endtime = datetime.datetime.now()
				if (response.status_code == 200):
					self.cnt_success += 1
					#print (response.content)
					self.total_time += (endtime - starttime).microseconds 
				else:
					self.cnt_fail += 1
				self.Print('GetUserProfile')

	def Start(self, func):
		self.cnt_success = 0
		self.cnt_fail = 0
		self.total_time = 0
		threads = []
		for i in range(P):
			t = threading.Thread(target=func, args=(self.clients[i], i))
			threads.append(t)

		for t in threads:
			t.setDaemon(True)
			t.start()
		for t in threads:
			t.join()
		sys.stdout.write('\n')

	def test(self):

		for i in range(P):
			c = Client()
			self.clients.append(c)
			self.thread_username.append(0)
		for i in range(N * P):
			self.username.append(random.randint(1000000000, 9999999999))
		self.Start(self.Register)
		self.Start(self.Active)
		self.Start(self.LogIn)
		self.Start(self.LogOut)
		self.Start(self.ChangePassword)
		self.Start(self.ChangeUserinfo)
		self.Start(self.AddTask)
		self.Start(self.ChangeTask)
		self.Start(self.AddTaskAction)
		self.Start(self.ChangeTaskAction)
		self.Start(self.RemoveTaskAction)
		self.Start(self.RemoveTask)
		self.Start(self.ResponseTask)
		self.Start(self.SelectTaskExecutor)
		self.Start(self.CloseTask)
		self.Start(self.CommentTask)
		self.Start(self.BrowseAllTask)
		self.Start(self.SeeTask)
		self.Start(self.SearchTask)
		self.Start(self.GetTaskActions)
		self.Start(self.OrderByTaskCompleted)
		self.Start(self.OrderByTaskCreated)
		self.Start(self.OrderByScores)
		self.Start(self.GetUserTask)
		self.Start(self.GetUserProfile)
		
		