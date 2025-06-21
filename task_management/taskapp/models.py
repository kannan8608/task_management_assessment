from django.db import models

# Create your models here.

# create task details
class TaskDetails(models.Model):
    title=models.CharField(max_length=100,blank=True,null=True)
    description=models.TextField()
    status=models.CharField(max_length=50,default='pending')
    due_date=models.DateField()
    #if user delete the task is_active field change Flase
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


