from django.contrib import admin
from .models import Account, Userinfo, Task, TaskAction
admin.site.register(Account)
admin.site.register(Userinfo)
admin.site.register(Task)
admin.site.register(TaskAction)
