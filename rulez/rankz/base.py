# -*- coding: utf-8 -*-

import inspect


class Rank(object):
    def __init__(self, display_name=None, has_rank=None, value=None):
        self._display = display_name
        self._value = value
        self._name = None
        self.has_rank = lambda user, obj: has_rank(self, user, obj)
    
    @property
    def name(self):
        if not self._name:
            raise NotImplemented
        
        return self._name
    
    @property
    def value(self):
        return self._value if self._value else self.name
    
    @property
    def display(self):
        return self._display if self._display else self.name
    
    def has_rank(self, user, obj):
        raise NotImplementedError


class RankingType(type):
    def __init__(cls, name, bases, namespace):
        cls._rankz = []
        cls.RANKS = []
        cls.CHOICES = []
        for name, value in namespace.items():
            if isinstance(value, Rank):
                value._name = name
                cls._rankz.append(value)
                cls.RANKS.append(name)
                cls.CHOICES.append((value.value, value.display))

    
class Ranking(object):
    __metaclass__ = RankingType
    
    @classmethod
    def get_rankz(cls):
        return cls._rankz
    
