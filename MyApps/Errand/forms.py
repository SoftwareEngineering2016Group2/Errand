from django import forms
 
def CheckUsername(username):
	if (username == None): return False
	if (len(username) != 10): return False
	return username.isdigit()
def CheckSex(sex):
	if (sex == None): return False
	if (len(sex) != 1):	return False
	if (sex[0] != 'M' and sex[0] != 'F'): return False
	return True
def CheckPhoneNumber(phone_number):
	if (phone_number == None): return False
	if (len(phone_number) != 11): return False
	return phone_number.isdigit()
def CheckScore(score):
	if (score == None): return False
	return (score >= 1 and score <= 5)
class RegisterForm(forms.Form):
	username = forms.CharField(max_length=10, label='username')
	password = forms.CharField(max_length=16, label='password')
	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		if (CheckUsername(cleaned_data.get('username')) == False):
			self._errors['username'] = self.error_class([''])

class ActiveForm(forms.Form):
	username = forms.CharField(max_length=10, label='username')
	password = forms.CharField(max_length=16, label='password')
	activecode = forms.CharField(max_length=4, label='activecode')

class LogInForm(forms.Form):
	username = forms.CharField(max_length=10, label='username')
	password = forms.CharField(max_length=16, label='password')

class ChangePasswordForm(forms.Form):
	username = forms.CharField(max_length=10, label='username')
	password = forms.CharField(max_length=16, label='password')
	newpassword = forms.CharField(max_length=16, label='newpassword')

class UserinfoForm(forms.Form):
	nickname = forms.CharField(max_length=16, label='nickname')
	sex = forms.CharField(max_length=1, label='sex')
	phone_number = forms.CharField(max_length=11, label='phone_number')
	birthday = forms.DateField(label='birthday')
	signature = forms.CharField(max_length=128, label="signature")
	def clean(self):
		cleaned_data = super(UserinfoForm, self).clean()
		if (CheckSex(cleaned_data.get('sex')) == False):
			self._errors['sex'] = self.error_class([''])
		if (CheckPhoneNumber(cleaned_data.get('phone_number')) == False):
			self._errors['phone_number'] = self.error_class([''])

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
	def clean(self):
		cleaned_data = super(CommentTaskForm, self).clean()
		if (CheckScore(cleaned_data.get('score')) == False):
			self._errors['score'] = self.error_class([''])

class BrowseAllTaskForm(forms.Form):
	pk = forms.CharField(max_length=16, label="Task ID")
	
class GetTaskActionsForm(forms.Form):
	pk = forms.CharField(max_length=16, label="Task ID")

class UploadPictureForm(forms.Form):
	image = forms.ImageField()