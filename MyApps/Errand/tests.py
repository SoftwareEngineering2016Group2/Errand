#!/usr/bin/python
# -*-coding:UTF-8 -*-
from django.test import TestCase
import urllib
import http.cookiejar as cookielib
from django.core.serializers import serialize,deserialize
from .models import Account, Userinfo, Task, TaskAction, TaskRelated
import json
import simplejson  
#??abount the csrf_exempt
cj = cookielib.CookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

HEADER = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
	'Referer' : 'http://202.206.1.163/logout.do'
}

url = 'http://127.0.0.1:8000/Errand/'
#send postdata and return response
#url = 'http://139.129.47.180:8002/Errand/'
def geturlopen(hosturl, postdata = {}, headers = HEADER):
	enpostdata = urllib.parse.urlencode(postdata).encode('utf-8') 
	urlrequest = urllib.request.Request(hosturl, enpostdata, headers)
	urlresponse = urllib.request.urlopen(urlrequest)
	return urlresponse
def getData(uri, data = {}):
	return geturlopen(url + uri, data).read().decode('utf-8')



account = [
{'username': '1234567890', 'password' : '123'},
{'username': '0987654321', 'password' : '456'},
{'username': '7890000000', 'password' : '789'}
]
userinfo = [
{'nickname':'Sun', 'sex' :'M', 'phone_number':'13888888888', 'birthday':'1994-10-11', 'signature':'Sleeping..'},
{'nickname':'Zhang', 'sex' :'F', 'phone_number':'13999999999', 'birthday':'1995-10-11', 'signature':'Eating..'},
{'nickname':'Sun', 'sex' :'M', 'birthday':'1994-10-11', 'signature':'Sleeping..'},
{'nickname':'Zhang', 'sex' :'F', 'birthday':'1995-10-11', 'signature':'Eating..'},
]
task = [
{'headline':'qu kuai di', 'detail':'bang wo qu kuai di', 'reward':'ji tui fan'},
{'headline':'dai fan', 'detail':'bang wo dai fan', 'reward':'5 yuan'}
]
taskAction = [
{'start_time' : '2011-10-11 12:00:00', 'end_time' : '2011-10-11 13:00:00', 'place' : 'er jiao', 'action' : 'gei wo'},
{'start_time' : '2016-10-11 13:00:00', 'end_time' : '2016-10-11 14:00:00', 'place' : 'yi jiao', 'action' : 'gei ni'},
]

class ViewsTestCase(TestCase):
	def Register(self):
		RSA = getData('')
		self.assertEqual(getData('register', account[0]), 'OK')
		self.assertEqual(getData('register', account[0]), 'FAILED : The username is existed.')
		self.assertEqual(getData('register', account[1]), 'OK')
		self.assertEqual(getData('register', account[1]), 'FAILED : The username is existed.')
	#only account 0 is activated
	def Active(self):
		RSA = getData('')
		self.assertEqual(getData('active', dict(account[0], **{'activecode':'1111'})), 'OK')
		self.assertEqual(getData('active', dict(account[1], **{'activecode':'2222'})), 'FAILED : Wrong Active Code')
		self.assertEqual(getData('active', dict(account[2], **{'activecode':'1111'})), 'FAILED : The username isn\'t existed, or wrong password.')
		#some double active issues here, but it seems alright
		self.assertEqual(getData('active', dict(account[0], **{'activecode':'1111'})), 'OK')
		#self.assertEqual(getData('active', dict(account[1], **{'activecode':'1111'})), 'OK')
	#account 0 login
	def LogIn(self):
		RSA = getData('')
		self.assertEqual(getData('login', account[0]), 'OK')
		self.assertEqual(getData('login', account[1]), 'FAILED : Please active account first.')
		self.assertEqual(getData('login', account[2]), 'FAILED : The username isn\'t existed, or wrong password.')
	
	def LogOut(self):
		self.assertEqual(getData('logout'), 'OK')
	#change password of account 0,1
	def ChangePassword(self):
		self.assertEqual(getData('changepassword', dict(account[0], **{'newpassword':'321'})), 'OK')
		self.assertEqual(getData('changepassword', dict(account[1], **{'newpassword':'654'})), 'OK')
		self.assertEqual(getData('changepassword', dict(account[2], **{'newpassword':'987'})), 'FAILED : The username isn\'t existed, or wrong password.')
		account[0]['password'] = '321'
		account[1]['password'] = '654'
	#change userinfo
	def ChangeUserinfo(self):
		self.assertEqual(getData('login', account[0]), 'OK')
		self.assertEqual(getData('changeuserinfo', userinfo[0]), 'OK')
		self.assertEqual(getData('login', account[1]), 'OK')
		self.assertEqual(getData('changeuserinfo', userinfo[1]), 'OK')
		self.assertEqual(getData('changeuserinfo', userinfo[0]), 'OK')
		self.assertEqual(simplejson.loads(getData('getmyuserinfo'))[0]['fields'], userinfo[0])
		self.assertEqual(getData('changeuserinfo', userinfo[1]), 'OK')

	def GetMyUserinfo(self):
		self.assertEqual(getData('login', account[0]), 'OK')
		self.assertEqual(simplejson.loads(getData('getmyuserinfo'))[0]['fields'], userinfo[0])
		self.assertEqual(getData('login', account[1]), 'OK')
		self.assertEqual(simplejson.loads(getData('getmyuserinfo'))[0]['fields'], userinfo[1])

	def TaskSteps(self):
		self.assertEqual(getData('login', account[0]), 'OK')
		mytask = simplejson.loads(getData('addtask', task[0]))[0]
		self.assertEqual(mytask['fields']['headline'], task[0]['headline'])
		mytask = simplejson.loads(getData('changetask', dict(task[1], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytask['fields']['headline'], task[1]['headline'])
		#check the taskCreated after a new task is created
		data = simplejson.loads(getData('orderbytaskcreated'))
		ret = [{"nickname": "John", "taskCreated": 1}, {"nickname": "John", "taskCreated": 0}]
		self.assertEqual(data,ret)
		
		mytaskaction = simplejson.loads(getData('addtaskaction', dict(taskAction[0], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[0]['place'])
		mytaskaction = simplejson.loads(getData('changetaskaction', dict(taskAction[1], **{'pk':mytaskaction['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[1]['place'])
		self.assertEqual(getData('removetaskaction', {'pk':mytaskaction['pk']}), 'OK')
		mytaskaction = simplejson.loads(getData('addtaskaction', dict(taskAction[0], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[0]['place'])
		mytaskaction = simplejson.loads(getData('changetaskaction', dict(taskAction[1], **{'pk':mytaskaction['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[1]['place'])
		self.assertEqual(getData('removetask', {'pk':mytask['pk']}), 'OK')		
		self.assertEqual(getData('removetaskaction', {'pk':mytaskaction['pk']}), 'FAILED : The task action isn\'t existed.')			
		self.assertEqual(getData('changetask', dict(task[1], **{'pk':mytask['pk']})), 'FAILED : The task isn\'t existed.')
		self.assertEqual(getData('removetask', {'pk':mytask['pk']}), 'FAILED : The task isn\'t existed.')
		
		#check after remove
		data = simplejson.loads(getData('orderbytaskcreated'))
		ret = [{"nickname": "John", "taskCreated": 0}, {"nickname": "John", "taskCreated": 0}]
		self.assertEqual(data,ret)
		
		#Waiting
		mytask = simplejson.loads(getData('addtask', task[0]))[0]
		self.assertEqual(mytask['fields']['headline'], task[0]['headline'])
		mytaskaction = simplejson.loads(getData('addtaskaction', dict(taskAction[0], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[0]['place'])
		self.assertEqual(getData('login', account[1]), 'OK')
		self.assertEqual(simplejson.loads(getData('getuserprofile', {'username':account[0]['username']})), userinfo[2])
		self.assertEqual(getData('responsetask', {'pk':mytask['pk']}), 'OK')
		self.assertEqual(simplejson.loads(getData('getuserprofile', {'username':account[0]['username']})), userinfo[2])
		self.assertEqual(getData('login', account[0]), 'OK')
		self.assertEqual(getData('selecttaskexecutor', {'pk':mytask['pk'], 'username':account[0]['username']}), 'FAILED : The user did\'t response the task.')
		self.assertEqual(getData('closetask', {'pk':mytask['pk']}), 'FAILED : You can\'t close the task.')		
		self.assertEqual(getData('commenttask', {'pk':mytask['pk'], 'score':5, 'comment':'Very Good'}), 'FAILED : You can\'t comment the task.')		
		self.assertEqual(getData('selecttaskexecutor', {'pk':mytask['pk'], 'username':account[1]['username']}), 'OK')		
		
		#Accepted
		self.assertEqual(getData('changetask', dict(task[1], **{'pk':mytask['pk']})), 'FAILED : You can\'t change the task.')
		self.assertEqual(getData('removetask', {'pk':mytask['pk']}), 'FAILED : You can\'t remove the task.')
		self.assertEqual(getData('changetaskaction', dict(taskAction[1], **{'pk':mytaskaction['pk']})), 'FAILED : You can\'t change the task action.')
		self.assertEqual(getData('removetaskaction', {'pk':mytaskaction['pk']}), 'FAILED : You can\'t remove the task action.')			
		self.assertEqual(getData('selecttaskexecutor', {'pk':mytask['pk'], 'username':account[1]['username']}), 'FAILED : You can\'t select executor for the task.')		
		self.assertEqual(getData('login', account[1]), 'OK')
		self.assertEqual(simplejson.loads(getData('getuserprofile', {'username':account[0]['username']}))[0]['fields'], userinfo[0])
		self.assertEqual(getData('responsetask', {'pk':mytask['pk']}), 'FAILED : You can\'t response the task.')
		self.assertEqual(getData('login', account[0]), 'OK')
		self.assertEqual(getData('commenttask', {'pk':mytask['pk'], 'score':5, 'comment':'Very Good'}), 'FAILED : You can\'t comment the task.')		
		self.assertEqual(getData('closetask', {'pk':mytask['pk']}), 'OK')	
		
		#Closed
		self.assertEqual(getData('changetask', dict(task[1], **{'pk':mytask['pk']})), 'FAILED : You can\'t change the task.')
		self.assertEqual(getData('removetask', {'pk':mytask['pk']}), 'FAILED : You can\'t remove the task.')
		self.assertEqual(getData('changetaskaction', dict(taskAction[1], **{'pk':mytaskaction['pk']})), 'FAILED : You can\'t change the task action.')
		self.assertEqual(getData('removetaskaction', {'pk':mytaskaction['pk']}), 'FAILED : You can\'t remove the task action.')			
		self.assertEqual(getData('selecttaskexecutor', {'pk':mytask['pk'], 'username':account[1]['username']}), 'FAILED : You can\'t select executor for the task.')		
		self.assertEqual(getData('login', account[1]), 'OK')
		self.assertEqual(simplejson.loads(getData('getuserprofile', {'username':account[0]['username']}))[0]['fields'], userinfo[0])
		self.assertEqual(getData('responsetask', {'pk':mytask['pk']}), 'FAILED : You can\'t response the task.')
		self.assertEqual(getData('login', account[0]), 'OK')
		self.assertEqual(getData('closetask', {'pk':mytask['pk']}), 'OK')		
		self.assertEqual(getData('commenttask', {'pk':mytask['pk'], 'score':5, 'comment':'Very Good'}), 'OK')		
		self.assertEqual(getData('login', account[1]), 'OK')		
		self.assertEqual(simplejson.loads(getData('getuserprofile', {'username':account[0]['username']}))[0]['fields'], userinfo[0])
	def TaskIsNotExist(self):
		mytask = simplejson.loads(getData('addtask', task[0]))[0]
		self.assertEqual(getData('changetask', dict(task[1], **{'pk':'-1'})), 'FAILED : The task isn\'t existed.')
		self.assertEqual(getData('removetask', {'pk':'-1'}), 'FAILED : The task isn\'t existed.')
		self.assertEqual(getData('changetaskaction', dict(taskAction[1], **{'pk':'-1'})), 'FAILED : The task action isn\'t existed.')
		self.assertEqual(getData('removetaskaction', {'pk':'-1'}), 'FAILED : The task action isn\'t existed.')			
		self.assertEqual(getData('responsetask', {'pk':'-1'}), 'FAILED : The task isn\'t existed.')
		self.assertEqual(getData('selecttaskexecutor', {'pk':'-1', 'username':account[1]['username']}), 'FAILED : The task isn\'t existed.')		
		self.assertEqual(getData('selecttaskexecutor', {'pk':mytask['pk'], 'username':account[2]['username']}), 'FAILED : The username isn\'t existed')
		self.assertEqual(getData('closetask', {'pk':'-1'}), 'FAILED : The task isn\'t existed.')		
		self.assertEqual(getData('closetask', {'pk':'-1'}), 'FAILED : The task isn\'t existed.')		
		self.assertEqual(getData('commenttask', {'pk':'-1', 'score':5, 'comment':'Very Good'}), 'FAILED : The task isn\'t existed.')		
	def Browse(self):
		self.assertEqual(getData('login', account[0]), 'OK')
		mytask = simplejson.loads(getData('addtask', task[0]))[0]
		self.assertEqual(mytask['fields']['headline'], task[0]['headline'])
		mytaskaction = simplejson.loads(getData('addtaskaction', dict(taskAction[0], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[0]['place'])
		mytaskaction = simplejson.loads(getData('addtaskaction', dict(taskAction[1], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[1]['place'])
		self.assertEqual(getData('responsetask', {'pk':mytask['pk']}), 'OK')
		self.assertEqual(getData('login', account[1]), 'OK')
		self.assertEqual(getData('responsetask', {'pk':mytask['pk']}), 'OK')
		tasks = getData('browsealltask', {'pk':'9999999'})
		mytask = simplejson.loads(tasks)[0]
		self.assertEqual(mytask['fields']['headline'], task[0]['headline'])
		taskactions = getData('gettaskactions', {'pk':mytask['pk']})
		mytaskaction = simplejson.loads(taskactions)[0]
		print (taskactions)
		self.assertEqual(mytaskaction['fields']['place'], taskAction[0]['place'])
		
	def CloseTasks(self):
		self.assertEqual(getData('login', account[0]), 'OK')
		mytask = simplejson.loads(getData('addtask', task[0]))[0]
		self.assertEqual(mytask['fields']['headline'], task[0]['headline'])
		mytaskaction = simplejson.loads(getData('addtaskaction', dict(taskAction[0], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[0]['place'])
		mytaskaction = simplejson.loads(getData('addtaskaction', dict(taskAction[1], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[1]['place'])
		
		mytask = simplejson.loads(getData('addtask', task[0]))[0]
		self.assertEqual(mytask['fields']['headline'], task[0]['headline'])
		mytaskaction = simplejson.loads(getData('addtaskaction', dict(taskAction[0], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[0]['place'])
		mytaskaction = simplejson.loads(getData('addtaskaction', dict(taskAction[1], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[1]['place'])
		

		mytask = simplejson.loads(getData('addtask', task[1]))[0]
		self.assertEqual(mytask['fields']['headline'], task[1]['headline'])
		mytaskaction = simplejson.loads(getData('addtaskaction', dict(taskAction[0], **{'pk':mytask['pk']})))[0]
		self.assertEqual(mytaskaction['fields']['place'], taskAction[0]['place'])
		
		tasks = simplejson.loads(getData('browsealltask', {'pk':'9999999'}))
		self.assertEqual(len(tasks), 5)

	def TaskPermission(self):
		pass
		
	def test(self):
		self.Register()
		self.Active()
		#self.LogIn()
		#self.LogOut()
		#self.ChangePassword()
		self.assertEqual(getData('active', dict(account[1], **{'activecode':'1111'})), 'OK')
		#self.ChangeUserinfo()
		#self.GetMyUserinfo()
		self.TaskSteps()
		self.TaskIsNotExist()
		self.TaskPermission()
		self.Browse()