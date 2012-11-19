"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rankzapp.models import MyTeam

class RankzTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user")
        self.userteam = MyTeam.objects.create(user=self.user,
                                               rank=MyTeam.ranking.leader.value)
    
    def test_userrankz(self):
        for rank in MyTeam.ranking._rankz:
            hasrank = True if self.userteam.rank == rank.value else False
            self.assertEqual(self.userteam.has_rank(self.user, rank), hasrank)

