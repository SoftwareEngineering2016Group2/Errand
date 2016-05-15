from django import forms
 
class RegisterForm(forms.Form):
	username = forms.CharField(max_length=16, label='username')
	password = forms.CharField(max_length=16, label='password')
	#nickname = forms.CharField(max_length=16, label='nickname')
class ActiveForm(forms.Form):
	username = forms.CharField(max_length=16, label='username')
	password = forms.CharField(max_length=16, label='password')
	activecode = forms.CharField(max_length=16, label='activecode')
class LogInForm(forms.Form):
	username = forms.CharField(max_length=16, label='username')
	password = forms.CharField(max_length=16, label='password')
class LogOutForm(forms.Form):
	username = forms.CharField(max_length=16, label='username')
	password = forms.CharField(max_length=16, label='password')
class ChangePasswordForm(forms.Form):
	username = forms.CharField(max_length=16, label='username')
	password = forms.CharField(max_length=16, label='password')
	newpassword = forms.CharField(max_length=16, label='newpassword')
class UserinfoForm(forms.Form):
	nickname = forms.CharField(max_length=16, label='nickname')
	sex = forms.CharField(max_length=1, label='sex')
	phone_number = forms.CharField(max_length=11, label='phone_number')
	birthday = forms.DateField(label='birthday')
	signature = forms.CharField(max_length=140, label="signature")

