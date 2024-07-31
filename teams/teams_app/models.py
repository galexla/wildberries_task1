from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=400)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    position = models.CharField(max_length=400)
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, related_name="members"
    )
