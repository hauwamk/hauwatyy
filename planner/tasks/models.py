

# Create your models here.
from django.db import models
#django provides a built-in User model that we can use to associate tasks with specific users.
#  We will import the User model from django.contrib.auth.models and
#  create a foreign key relationship between the Task model and the User model. 
# This way, each task will be linked to a specific user, 
# allowing us to manage tasks on a per-user basis.
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    time = models.CharField(max_length=50)
#new tasks are not completed by default
    completed = models.BooleanField(default=False)

    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name   