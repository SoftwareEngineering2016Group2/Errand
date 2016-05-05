from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.account_controller.RSA),
	url(r'^register$', views.account_controller.Register),
	url(r'^active$', views.account_controller.Active),
	url(r'^login$', views.account_controller.LogIn),
	url(r'^logout$', views.account_controller.LogOut),
	url(r'^changepassword$', views.account_controller.ChangePassword),
	#url(r'^register')
]