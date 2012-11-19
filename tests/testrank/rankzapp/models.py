# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from .rules import rankz, MyTeamRanking


@rankz(MyTeamRanking)
class MyTeam(models.Model):
    user = models.ForeignKey(User)
    rank = models.SmallIntegerField(choices=MyTeamRanking.CHOICES,
                                    default=MyTeamRanking.fellow.value)

