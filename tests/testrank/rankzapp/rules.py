# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from rulez.rankz.base import Rank, Ranking
from rulez.rankz.utils import rankz


def myteam_has_rank(rank, user, obj):
    return obj.user == user and obj.rank == rank.value


class MyTeamRanking(Ranking):
    leader = Rank(display_name=_(u"leader"), has_rank=myteam_has_rank, value=3)
    fellow = Rank(_(u"fellow"), myteam_has_rank, 2)
    viewer = Rank(_(u"viewer"), myteam_has_rank, 1)
    inactive = Rank(_(u"inactive"), myteam_has_rank, 0)

