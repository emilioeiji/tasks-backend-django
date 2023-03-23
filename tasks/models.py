from django.contrib.auth.models import User
from django.db import models


class Tasks(models.Model):
    desc = models.CharField(max_length=100)
    estimateAt = models.DateField()
    doneAt = models.DateField(blank=True, null=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.desc)
