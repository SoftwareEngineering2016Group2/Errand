from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.account_controller.RSA),
	url(r'^register$', views.account_controller.Register),
	url(r'^active$', views.account_controller.Active),
	url(r'^login$', views.account_controller.LogIn),
	url(r'^logout$', views.account_controller.LogOut),
	url(r'^changepassword$', views.account_controller.ChangePassword),
	url(r'^changeuserinfo$', views.userinfo_controller.ChangeUserinfo),
	url(r'^getuserinfo$', views.userinfo_controller.GetUserinfo),
	url(r'^addtask$', views.task_controller.AddTask),
	url(r'^addtaskaction$', views.task_controller.AddTaskAction),
	url(r'^changetaskaction$', views.task_controller.ChangeTaskAction),
	url(r'^removetaskaction$', views.task_controller.RemoveTaskAction),
	#url(r'^register')
]