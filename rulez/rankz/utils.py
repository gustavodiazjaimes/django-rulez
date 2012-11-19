# -*- coding: utf-8 -*-

from rulez.utils import rulez

from .cache import cache_get_rankz, stamp_rubber
from .signals import signals


@cache_get_rankz
def get_rankz(self, user=None):
    if not user:
        return self.rankz
    
    user_rankz = []
    for rank in self.ranking.get_rankz():
        if rank.has_rank(user, self):
            user_rankz.append(rank)
    
    return user_rankz

def has_rank(self, user, rank):
    user_rankz = self.get_rankz(user)
    if rank in user_rankz:
        return True
    return False

def rulez_invalidate(self):
    stamp_rubber(self)


class rankz(object):
    def __init__(self, ranking):
        # assert(isinstance(ranking, Ranking))
        self.ranking = ranking

    def __call__(self, cls):
        cls.ranking = self.ranking
        cls.get_rankz = get_rankz
        cls.has_rank = has_rank
        cls.rulez_invalidate = rulez_invalidate
        
        return rulez()(cls)

