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


def RSA_valid(Fn):
	def Delegator(self, request):
		pubkey = request.session.get('pubkey', None)
		privkey = request.session.get('privkey', None)
		if privkey == None:
			return HttpResponse('Please request for RSA')
		return Fn(self, request)
	return Delegator

def Logged_in(Fn):
	def Delegator(self, request):
		username = request.session.get('username', None)
		if username == None:
			return HttpResponse('Please log in.')
		return Fn(self, request)
	return Delegator

def FormValid(request, form_model):
	form = form_model(request.POST)
	return form.is_valid(), form.cleaned_data

	
class Userinfo_Controller:

	def CreateUserinfo(self):
		return Userinfo.objects.create()
		
	@csrf_exempt
	@Logged_in
	def GetUserinfo(self, request):
		userinfo = account_controller.FindByUsername(request.session['username']).userinfo
		#print (userinfo)
		return HttpResponse(userinfo.ToJSON())
	
	@csrf_exempt
	@Logged_in
	def ChangeUserinfo(self, request):
		valid, data = FormValid(request, forms.UserinfoForm)
		if (valid == False):
			return HttpResponse('Form format error.')
		userinfo = account_controller.FindByUsername(request.session['username']).userinfo
		userinfo.ChangeUserinfo(data)
		return HttpResponse('ChangeuUserinfo successfully.')

userinfo_controller = Userinfo_Controller()



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
		#activecode = random.randint(1000, 9999)
		userinfo = userinfo_controller.CreateUserinfo()
		print (userinfo.nickname, userinfo.sex, userinfo.birthday, userinfo.signature)
		activecode = 1111
		account, created = Account.objects.get_or_create(username=username,
			defaults = {'password' : password, 'activecode' : activecode, 'userinfo' : userinfo})
		#print (created)
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
			return HttpResponse('Form format error.')

		account, created = self.CreateAccount(data['username'], data['password'])
		if (created):
			return HttpResponse("We have sent an active-code to your PKU mail.")
		else:
			return HttpResponse('The username is existed.')

	@csrf_exempt
	@RSA_valid
	def Active(self, request):
		valid, data = FormValid(request, forms.ActiveForm)
		if (valid == False):
			return HttpResponse('Form format error.')
		account = self.FindByUsernameAndPassword(data['username'], data['password'])
		if account == None:
			return HttpResponse('The username isn\'t existed, or wrong password.' )
		elif account.Active(data['activecode']) == True:
			return HttpResponse(account.userinfo.nickname)
		else:
			return HttpResponse('Wrong Activecode.')

	@csrf_exempt
	@RSA_valid
	def LogIn(self, request):
		valid, data = FormValid(request, forms.LogInForm)
		if (valid == False):
			return HttpResponse('Form format error.')
		account = self.FindByUsernameAndPassword(data['username'], data['password'])	
		if account == None:
			return HttpResponse('The username isn\'t existed, or wrong password.' )
		elif account.active == False:
			self.SendEmail(account.username, account.activecode)
			return HttpResponse('Please active account first. We have sent the active code to your email.')
		else:
			request.session['username'] = account.username
			return HttpResponse('Log in successfully.')

	@csrf_exempt
	@RSA_valid
	def LogOut(self, request):
		valid, data = FormValid(request, forms.LogOutForm)
		if (valid == False):
			return HttpResponse('Form format error.')
		account = self.FindByUsernameAndPassword(data['username'], data['password'])	
		if account == None:
			return HttpResponse('The username isn\'t existed, or wrong password.' )
		else:
			request.session['username'] = None
			return HttpResponse('Log out successfully.')

	@csrf_exempt
	@RSA_valid
	def ChangePassword(self, request):
		valid, data = FormValid(request, forms.ChangePasswordForm)
		if (valid == False):
			return HttpResponse('Form format error.')
		account = self.FindByUsernameAndPassword(data['username'], data['password'])	
		if account == None:
			return HttpResponse('The username isn\'t existed, or wrong password.' )
		else:
			account.ChangePassword(data['newpassword'])
			return HttpResponse('Change password successfully.')


account_controller = Account_Controller()