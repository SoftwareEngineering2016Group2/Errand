from django.shortcuts import render
from django.http import HttpResponse
import rsa
from . import forms
from .models import Account, Userinfo, Task, TaskAction, TaskRelated
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core import serializers
from django.utils import timezone
from django.db import transaction
import json
import random

#----- This Delegator is used to judge if RSA key is generated -----
def RSA_valid(Fn):
	def Delegator(self, request):
		pubkey = request.session.get('pubkey', None)
		privkey = request.session.get('privkey', None)
		if privkey == None:
			return HttpResponse('Please request for RSA')
		return Fn(self, request)
	return Delegator

#----- This Delegator is used to judge if the user is logged in -----
def Logged_in(Fn):
	def Delegator(self, request):
		username = request.session.get('username', None)
		if username == None:
			return HttpResponse('Please log in.')
		return Fn(self, request)
	return Delegator

#----- Verify the legitimacy of the form -----
def FormValid(request, form_model):
	form = form_model(request.POST)
	return form.is_valid(), form.cleaned_data


#----- Class : Task Controller -----
class Task_Controller:
	def FindTask(self, pk):
		try:
			task = Task.objects.select_for_update().get(pk=pk)
		except Task.DoesNotExist:
			task = None
		return task

	def CreateTask(self, create_account, data):
		return Task.objects.create(create_account=create_account, create_time=timezone.now(), \
			headline=data['headline'], detail=data['detail'], reward=data['reward'])

	@csrf_exempt
	@Logged_in
	def AddTask(self, request):
		valid, data = FormValid(request, forms.AddTaskForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		account = account_controller.FindByUsername(request.session['username'])
		#update the taskCreated
		with transaction.atomic():
			account.taskRelated.updateTaskCreated()
		task = self.CreateTask(account, data)
		return HttpResponse(serializers.serialize("json", [task]))


	@csrf_exempt
	@Logged_in
	def ChangeTask(self, request):
		valid, data = FormValid(request, forms.ChangeTaskForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			task = self.FindTask(data['pk'])	
			if (task == None):
				return HttpResponse('FAILED : The task isn\'t existed.' )
			if (task.CanChange(request.session.get('username', None)) == False):
				return HttpResponse('FAILED : You can\'t change the task.')
			task.ChangeTask(data)
			return HttpResponse(serializers.serialize("json", [task]))
	
	@csrf_exempt
	@Logged_in
	def RemoveTask(self, request):
		valid, data = FormValid(request, forms.RemoveTaskForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			task = self.FindTask(data['pk'])	
			if (task == None):
				return HttpResponse('FAILED : The task isn\'t existed.' )
			if (task.CanChange(request.session.get('username', None)) == False):
				return HttpResponse('FAILED : You can\'t remove the task.')
			#update the taskCreated and the taskCompleted and scores
			with transaction.atomic():
				task.create_account.taskRelated.updateTaskCreated(-1)
				if task.execute_account != None:
				#if hasattr(task, 'execute_account'):
					task.execute_account.taskRelated.updateTaskCompleted(-1)
					if not task.scoreDefault():
						task.execute_account.taskRelated.updateScores(-task.scores)
			task.delete()
			return HttpResponse('OK')

	def FindTaskAction(self, pk):
		try:
			taskAction = TaskAction.objects.select_for_update().get(pk=pk)
		except TaskAction.DoesNotExist:
			taskAction = None
		return taskAction

	def CreateTaskAction(self, task, data):
		return TaskAction.objects.create(task_belong=task, action=data['action'], \
			start_time=data['start_time'], end_time=data['end_time'], place=data['place'])

	@csrf_exempt
	@Logged_in
	def AddTaskAction(self, request):
		valid, data = FormValid(request, forms.AddTaskActionForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			task = self.FindTask(data['pk'])	
			if (task == None):
				return HttpResponse('FAILED : The task isn\'t existed.')
			if (task.CanChange(request.session.get('username', None)) == False):
				return HttpResponse('FAILED : You can\'t change the task.')
			if (task.task_actions.count() > 5):
				return HttpResponse("FAILED : The task have too many actions.")
			taskAction = self.CreateTaskAction(task, data)
			return HttpResponse(serializers.serialize("json", [taskAction]))

	@csrf_exempt
	@Logged_in
	def ChangeTaskAction(self, request):
		valid, data = FormValid(request, forms.ChangeTaskActionForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			taskAction = self.FindTaskAction(data['pk'])	
			if (taskAction == None):
				return HttpResponse('FAILED : The task action isn\'t existed.')
			task = taskAction.task_belong;
			if (task.CanChange(request.session.get('username', None)) == False):
				return HttpResponse('FAILED : You can\'t change the task action.')
			taskAction.ChangeTaskAction(data)
			return HttpResponse(serializers.serialize("json", [taskAction]))
		
	@csrf_exempt
	@Logged_in
	def RemoveTaskAction(self, request):
		valid, data = FormValid(request, forms.RemoveTaskActionForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			taskAction = self.FindTaskAction(data['pk'])	
			if (taskAction == None):
				return HttpResponse('FAILED : The task action isn\'t existed.')
			task = taskAction.task_belong;
			if (task.CanChange(request.session.get('username', None)) == False):
				return HttpResponse('FAILED : You can\'t remove the task action.')
			taskAction.delete()
			return HttpResponse('OK')

	@csrf_exempt
	@Logged_in
	def ResponseTask(self, request):
		valid, data = FormValid(request, forms.ResponseTaskForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			task = self.FindTask(data['pk'])
			account = account_controller.FindByUsername(request.session['username'])
			if (task == None):
				return HttpResponse('FAILED : The task isn\'t existed.' )
			if (task.InWaiting() == False):
				return HttpResponse('FAILED : You can\'t response the task.')
			task.response_accounts.add(account)
			return HttpResponse('OK')

	@csrf_exempt
	@Logged_in
	def SelectTaskExecutor(self, request):
		valid, data = FormValid(request, forms.SelectTaskExecutorForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			task = self.FindTask(data['pk'])
			if (task == None):
				return HttpResponse('FAILED : The task isn\'t existed.' )
			account = account_controller.FindByUsername(data['username'])
			if account == None:
				return HttpResponse('FAILED : The username isn\'t existed')
			if (task.CanSelect(request.session.get('username', None)) == False):
				return HttpResponse('FAILED : You can\'t select executor for the task.')
			try:
				response_account = task.response_accounts.get(username=data['username'])
			except Account.DoesNotExist:
				response_account = None
			if (response_account == None):
				return HttpResponse('FAILED : The user did\'t response the task.')
			task.Accept(response_account)
			return HttpResponse('OK')

	@csrf_exempt
	@Logged_in
	def CloseTask(self, request):
		valid, data = FormValid(request, forms.CloseTaskForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			task = self.FindTask(data['pk'])
			if (task == None):
				return HttpResponse('FAILED : The task isn\'t existed.')
			if (task.CanClose(request.session.get('username', None)) == False):
				return HttpResponse('FAILED : You can\'t close the task.')
			task.Close()
			#update taskCompleted of the execute_account
			with transaction.atomic():
				task.execute_account.taskRelated.updateTaskCompleted()
			return HttpResponse('OK')
	
	@csrf_exempt
	@Logged_in
	def CommentTask(self, request):
		valid, data = FormValid(request, forms.CommentTaskForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			task = self.FindTask(data['pk'])
			if (task == None):
				return HttpResponse('FAILED : The task isn\'t existed.')
			if (task.CanComment(request.session.get('username', None)) == False):
				return HttpResponse('FAILED : You can\'t comment the task.')
			#if the task has been commented, subtract the score
			with transaction.atomic():
				if not task.scoreDefault():
					task.execute_account.taskRelated.updateScores[-task.getScore()]
			
			task.Comment(data)
			#update the score
			with transaction.atomic():
				task.execute_account.taskRelated.updateScores(data['score'])
			return HttpResponse('OK')

	@csrf_exempt
	@Logged_in
	def BrowseAllTask(self, request):
		valid, data = FormValid(request, forms.BrowseAllTaskForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			tasks = Task.objects.filter(status='W', pk__lt=data['pk']).order_by('-pk')
			if (tasks.count() < 5):
				num = tasks.count()
			else: num = 5
			return HttpResponse(serializers.serialize("json", tasks[0:num]))
	
	@csrf_exempt
	@Logged_in
	def GetTaskActions(self, request):
		valid, data = FormValid(request, forms.GetTaskActionsForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			task = self.FindTask(data['pk'])
			if (task == None):
				return HttpResponse('FAILED : The task isn\'t existed.')
			return HttpResponse(serializers.serialize("json", task.task_actions.all()))
	#nedd to test chinese??
	@csrf_exempt
	@Logged_in
	def SearchTask(self, request):
		valid, data = FormValid(request,form.SearchTaskForm)
		if(valid == False):
			return HttpResponse('Form format error')
		text = data['text']
		result = Task.objects.filter(status='W',pk__lt=data['pk']).order_by('-pk')
		result = result.filter(Q(headline__contains=text)|Q(detail__contains=text))		
		if (result.count() < 5):
				num = result.count()
		else: num = 5
		return HttpResponse(serializers.serialize("json", result[0:num]))


task_controller = Task_Controller();
#----- End of Task Controller -----


#----- Class : Userinfo Controller -----
class Userinfo_Controller:

	def CreateUserinfo(self):
		return Userinfo.objects.create()

	@csrf_exempt
	@Logged_in
	def GetMyUserinfo(self, request):
		with transaction.atomic():
			userinfo = account_controller.FindByUsername(request.session['username']).userinfo
			return HttpResponse(serializers.serialize("json", [userinfo]))
	
	@csrf_exempt
	@Logged_in
	def ChangeUserinfo(self, request):
		valid, data = FormValid(request, forms.UserinfoForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			userinfo = account_controller.FindByUsername(request.session['username']).userinfo
			userinfo.ChangeUserinfo(data)
			return HttpResponse('OK')	
	@Logged_in
	@csrf_exempt	
	def ChangeAvatar(self, request):
		if request.method == 'POST':
			form = forms.AvatarUploadForm(request.POST,request.FILES)
			if form.is_valid():
				userinfo = account_controller.FindByUsername(request.session['username']).userinfo
				userinfo.ChangeAvatar(form.cleaned_data['image'])
				return HttpResponse('image upload success')
			else:
				return HttpResponse('Form format error!')
		return HttpResponse('allowed only via POST')
	#not finished yet??
	@Logged_in
	@csrf_exempt
	def GetUserInfo(self, request):
		valid, data = FormValid(request, forms.GetUserInfoForm)
		if(valid==False):
			return HttpResponse('FAILED : Form format error.')
		myAccount = account_controller.FindByUsername(request.session['username'])
		try:
			target = accounts_account_controller.FindByUsername(data['pk'])
		except Account.DoesNotExist:
			return HttpResponse('Target user does not exist')
		relatedUser1 = Task.objects.filter(execute_account=myAccount).values['create_account']
		relatedUser2 = Task.objects.filter(create_account=myAccount).values['execute_account']
		relatedUser = relatedUser2|relatedUser1|myAccount 
		if target in relatedUser:
			return HttpResponse(serializers.serialize("json", [target.userinfo]))
		else:
			return HttpResponse(serializers.serialize("json", [target.userinfo.deger('phone_number')]))


userinfo_controller = Userinfo_Controller()
#----- End of Userinfo Controller -----

#----- Class : Account Controller -----
class Account_Controller:

	def FindByUsername(self, username):
		try:
			account = Account.objects.select_for_update().get(username=username)
		except Account.DoesNotExist:
			account = None
		return account

	def FindByUsernameAndPassword(self, username, password):
		try:
			account = Account.objects.select_for_update().get(username=username, password=password)
		except Account.DoesNotExist:
			account = None
		return account

	def CreateAccount(self, username, password):
		#activecode = random.randint(1000, 9999)
		userinfo = userinfo_controller.CreateUserinfo()
		taskRelated = taskRelated_controller.CreateTaskRelated()
		activecode = 1111
		account, created = Account.objects.get_or_create(username=username,
			defaults = {'password' : password, 'activecode' : activecode, 'userinfo' : userinfo,'taskRelated':taskRelated})
		if (created):
			self.SendEmail(username, activecode)
		else:
			userinfo.delete()
		return account, created

	def SendEmail(self, username, activecode):
		email =  username + '@pku.edu.cn'
		subject, form_email, to = u'Errand Account Active', 'sunmengdexiaohao1@163.com', email
		text_content = 'Please input the code in Errand to active your account : ' + str(activecode)
		msg = EmailMultiAlternatives(subject, text_content, form_email, [to])
		msg.send()

	@csrf_exempt
	def RSA(self, request):
		(pubkey, privkey) = rsa.newkeys(1024)
		request.session['pubkey'] = pubkey
		request.session['privkey'] = privkey
		'''return render(request, 'Errand/index.html', {
           'form': forms.UserinfoForm,
        })'''
		return HttpResponse(pubkey)

	@csrf_exempt
	@RSA_valid
	def Register(self, request):
		valid, data = FormValid(request, forms.RegisterForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			account, created = self.CreateAccount(data['username'], data['password'])
			if (created):
				return HttpResponse('OK')
			else:
				return HttpResponse('FAILED : The username is existed.')

	@csrf_exempt
	@RSA_valid
	def Active(self, request):
		valid, data = FormValid(request, forms.ActiveForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			account = self.FindByUsernameAndPassword(data['username'], data['password'])
			if account == None:
				return HttpResponse('FAILED : The username isn\'t existed, or wrong password.')
			elif account.Active(data['activecode']) == True:
				return HttpResponse('OK')
			else:
				return HttpResponse('FAILED : Wrong Active Code')

	@csrf_exempt
	@RSA_valid
	def LogIn(self, request):
		valid, data = FormValid(request, forms.LogInForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			account = self.FindByUsernameAndPassword(data['username'], data['password'])	
			if account == None:
				return HttpResponse('FAILED : The username isn\'t existed, or wrong password.')
			elif account.active == False:
				self.SendEmail(account.username, account.activecode)
				return HttpResponse('FAILED : Please active account first.')
			else:
				request.session['username'] = account.username
				return HttpResponse('OK')

	@csrf_exempt
	def LogOut(self, request):
		request.session['username'] = None
		return HttpResponse('OK')
	#to change the password, login is not required
	@csrf_exempt
	@RSA_valid
	def ChangePassword(self, request):
		valid, data = FormValid(request, forms.ChangePasswordForm)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		with transaction.atomic():
			account = self.FindByUsernameAndPassword(data['username'], data['password'])	
			if account == None:
				return HttpResponse('FAILED : The username isn\'t existed, or wrong password.')
			else:
				account.ChangePassword(data['newpassword'])
				return HttpResponse('OK')

account_controller = Account_Controller()
#----- End of Account Controller -----
class TaskRelated_Controller:
	def CreateTaskRelated(self):
		return TaskRelated.objects.create()
	@csrf_exempt
	def OrderByTaskCompleted(self, request):
		with transaction.atomic():
			accounts = Account.objects.order_by('-taskRelated__taskCompleted')
			if (accounts.count() < 5):
				num = accounts.count()
			else: num = 5
			ret = {}
			return HttpResponse(serializers.serialize("json", accounts, fields = ('userinfo__nickname', 'taskRelated__taskCompleted')))
	@csrf_exempt
	def OrderByTaskCreated(self, request):
		with transaction.atomic():
			accounts = Account.objects.order_by('-taskRelated__taskCreated')
			if (accounts.count() < 5):
				num = accounts.count()
			else: num = 5
		ret = accounts.values('userinfo__nickname','taskRelated__taskCreated')
		list_result = [entry for entry in ret]
		for entry in list_result:
			entry['nickname'] = entry.pop('userinfo__nickname')
			entry['taskCreated'] = entry.pop('taskRelated__taskCreated')
		return HttpResponse(json.dumps(list_result))
	@csrf_exempt
	def OrderByScores(self, request):
		with transaction.atomic():
			accounts = Account.objects.order_by('-taskRelated__scores')
			if (accounts.count() < 5):
				num = accounts.count()
			else: num = 5
			return HttpResponse(serializers.serialize("json", accounts, fields = ('userinfo__nickname', 'taskRelated__scores')))
	
	@csrf_exempt
	def GetUserTask(self, request):
		valid, data = FormValid(request, forms.GetUserTask)
		if (valid == False):
			return HttpResponse('FAILED : Form format error.')
		typeOfTask = data['typeOfTask']
		state = data['state']
		username = data['username']
		myAccount = account_controller.FindByUsername(username)
		with transaction.atomic():
			if typeOfTask == 'execute_account':
				tasks = Task.objects.filter(status=state, execute_account=myAccount ,pk__lt=data['pk']).order_by('-pk')
			else:
				tasks = Task.objects.filter(status=state, create_account=myAccount ,pk__lt=data['pk']).order_by('-pk')
			if (tasks.count() < 5):
				num = tasks.count()
			else: num = 5
			return HttpResponse(serializers.serialize("json", tasks[0:num]))
##()
taskRelated_controller = TaskRelated_Controller()