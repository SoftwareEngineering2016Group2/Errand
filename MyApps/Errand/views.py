from django.shortcuts import render
from django.http import HttpResponse
import rsa
from . import forms
from .models import Account, Userinfo
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import random

'''
def form_valid(form_model,request):
	form = form_model(request.POST);
	if form.is_valid():
		def Delegator(Fn):
			return Fn
	else:
		def Delegator(Fn):
			def InvalidForm(self, request):
				return HttpResponse('Form format error.')
			return InvalidForm
	return Delegator(Fn)'''




def FormValid(request, form_model):
	form = form_model(request.POST)
	return form.is_valid()
	
class Userinfo_Controller:

	def CreateUserinfo(self):
		return Userinfo.objects.create()

userinfo_controller = Userinfo_Controller()


def RSA_valid(Fn):
	def Delegator(self, request):
		pubkey = request.session.get('pubkey', None)
		privkey = request.session.get('privkey', None)
		if privkey == None:
			return HttpResponse('Please request for RSA')
		return Fn(self, request)
	return Delegator
class Account_Controller:

	def FindByUsername(self, username):
		try:
			account = Account.objects.get(username=username)
		except Account.DoesNotExist:
			account = None
		return account

	def FindByUsernameAndPassword(self, username, password):
		try:
			account = Account.objects.get(username=username, password=password)
		except Account.DoesNotExist:
			account = None
		return account

	def CreateAccount(self, username, password):
		#newrole = role.objects.create(nickname=nickname)
		#activecode = random.randint(1000, 9999)
		userinfo = userinfo_controller.CreateUserinfo()
		activecode = 1111
		account, created = Account.objects.get_or_create(username=username,
			defaults = {'password' : password, 'activecode' : activecode, 'userinfo' : userinfo})
		print (created)
		if (created):
			self.SendEmail(username, activecode)
		else:
			userinfo.delete()
		return account, created

	def SendEmail(self, username, activecode):
		email =  username + '@pku.edu.cn'
		subject, form_email, to = u'Errand Account Active', 'sunmeng94@163.com', email
		text_content = 'Please input the code in Errand to active your account : ' + str(activecode)
		msg = EmailMultiAlternatives(subject, text_content, form_email, [to])
		msg.send()


	def RSA(self, request):
		(pubkey, privkey) = rsa.newkeys(1024)
		request.session['pubkey'] = pubkey
		request.session['privkey'] = privkey
		return HttpResponse(pubkey)

	@csrf_exempt
	@RSA_valid
	def Register(self, request):
		if (FormValid(request, forms.RegisterForm) == False):
			return HttpResponse('Form format error.')
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		#nickname = request.POST.get('nickname', '')

		account, created = self.CreateAccount(username, password)
		if (created):
			return HttpResponse("We have sent an active-code to your PKU mail.")
		else:
			return HttpResponse('The username is existed.')

	@csrf_exempt
	@RSA_valid
	def Active(self, request):
		if (FormValid(request, forms.ActiveForm) == False):
			return HttpResponse('Form format error.')
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		activecode = request.POST.get('activecode', '')
		account = self.FindByUsernameAndPassword(username, password)
		if account == None:
			return HttpResponse('The username isn\'t existed, or wrong password.' )
		elif account.Active(activecode) == True:
			return HttpResponse(account.userinfo.nickname)
		else:
			return HttpResponse('Wrong Activecode.')

	@csrf_exempt
	@RSA_valid
	def LogIn(self, request):
		if (FormValid(request, forms.LogInForm) == False):
			return HttpResponse('Form format error.')
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		account = self.FindByUsernameAndPassword(username, password)	
		if account == None:
			return HttpResponse('The username isn\'t existed, or wrong password.' )
		elif account.active == False:
			self.SendEmail(account.username, account.activecode)
			return HttpResponse('Please active account first. We have sent the active code to your email.')
		else:
			#request.session['role'] = myaccount.role
			return HttpResponse('Log in successfully.')
	@csrf_exempt
	@RSA_valid
	def LogOut(self, request):
		if (FormValid(request, forms.LogOutForm) == False):
			return HttpResponse('Form format error.')
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		account = self.FindByUsernameAndPassword(username, password)	
		if account == None:
			return HttpResponse('The username isn\'t existed, or wrong password.' )
		else:
			#request.session['role'] = myaccount.role
			return HttpResponse('Log out successfully.')

	@csrf_exempt
	@RSA_valid
	def ChangePassword(self, request):
		if (FormValid(request, forms.ChangePasswordForm) == False):
			return HttpResponse('Form format error.')
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		newpassword = request.POST.get('newpassword', '')
		account = self.FindByUsernameAndPassword(username, password)	
		if account == None:
			return HttpResponse('The username isn\'t existed, or wrong password.' )
		else:
			account.ChangePassword(newpassword)
			return HttpResponse('Change password successfully.')


account_controller = Account_Controller()