from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=400, unique=True)


class Member(models.Model):
    name = models.CharField(max_length=400)
    position = models.CharField(max_length=400)
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, related_name="members"
    )
