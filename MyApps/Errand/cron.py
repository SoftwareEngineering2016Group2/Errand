from .models import Account, Userinfo, Task, TaskAction
from django.utils import timezone
from django.db import transaction
def CloseTasks():
	with transaction.atomic():
		tasks = Task.objects.select_for_update().exclude(task_actions__end_time__gt=timezone.localtime(timezone.now())).exclude(status='C')
		for task in tasks:
			task.Close()
	