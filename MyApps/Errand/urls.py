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
	url(r'^getmyuserinfo$', views.userinfo_controller.GetMyUserinfo),
	url(r'^addtask$', views.task_controller.AddTask),
	url(r'^changetask$', views.task_controller.ChangeTask),
	url(r'^removetask$', views.task_controller.RemoveTask),
	url(r'^addtaskaction$', views.task_controller.AddTaskAction),
	url(r'^changetaskaction$', views.task_controller.ChangeTaskAction),
	url(r'^removetaskaction$', views.task_controller.RemoveTaskAction),
	url(r'^responsetask$', views.task_controller.ResponseTask),
	url(r'^selecttaskexecutor$', views.task_controller.SelectTaskExecutor),
	url(r'^closetask$', views.task_controller.CloseTask),
	url(r'^commenttask$', views.task_controller.CommentTask),
	url(r'^browsealltask$', views.task_controller.BrowseAllTask),
]