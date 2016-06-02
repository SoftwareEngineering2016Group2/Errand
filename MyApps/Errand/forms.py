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

class AvatarUploadForm(forms.Form):
	avatar = forms.ImageField()
	
class AddTaskForm(forms.Form):
	headline = forms.CharField(max_length=16, label='Headline')
	detail = forms.CharField(max_length=128, label='Detail')
	reward = forms.CharField(max_length=16, label='Reward')

class ChangeTaskForm(forms.Form):
	pk = forms.CharField(max_length=16, label="Task ID")
	headline = forms.CharField(max_length=16, label='Headline')
	detail = forms.CharField(max_length=128, label='Detail')
	reward = forms.CharField(max_length=16, label='Reward')

class RemoveTaskForm(forms.Form):
	pk = forms.CharField(max_length=16, label="Task ID")

class AddTaskActionForm(forms.Form):
	pk = forms.CharField(max_length=16, label="Task ID")
	start_time = forms.DateTimeField(label='Start Time')
	end_time = forms.DateTimeField(label='End Time')
	place = forms.CharField(max_length=16, label='Place')
	action = forms.CharField(max_length=50, label='Action')

class ChangeTaskActionForm(forms.Form):
	pk = forms.CharField(max_length=16, label="TaskAction ID")
	start_time = forms.DateTimeField(label='Start Time')
	end_time = forms.DateTimeField(label='End Time')
	place = forms.CharField(max_length=16, label='Place')
	action = forms.CharField(max_length=50, label='Action')

class RemoveTaskActionForm(forms.Form):
	pk = forms.CharField(max_length=16, label="TaskAction ID")

class ResponseTaskForm(forms.Form):
	pk = forms.CharField(max_length=16, label="Task ID")

class SelectTaskExecutorForm(forms.Form):
	pk = forms.CharField(max_length=16, label="Task ID")
	username = forms.CharField(max_length=16, label="Executor Name")

class CloseTaskForm(forms.Form):
	pk = forms.CharField(max_length=16, label="Task ID")

class CommentTaskForm(forms.Form):
	pk = forms.CharField(max_length=16, label="Task ID")
	score = forms.IntegerField(label="Score")
	comment = forms.CharField(max_length=128, label='Detail')

class BrowseAllTaskForm(forms.Form):
	pk = forms.CharField(max_length=16, label="Task ID")
