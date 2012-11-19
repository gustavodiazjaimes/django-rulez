#-*- coding: utf-8 -*-

import time

from django.core.cache import cache
from django.utils.functional import wraps
from django.contrib.auth.models import User, AnonymousUser

"""
Cache keys:

For the list of roles, per user, per instance:
<prefix>-<user.id>-<user counter>-<obj.type>-<obj.id>-<obj counter>

For the counter , per instance:
<prefix>-<obj.type>-<obj.id>

"""

#===============================================================================
# Utils
#===============================================================================

CACHE_TIME = 0
ANONYMOUS = 'A0'

def get_user_pk(user):
    if user and user.is_authenticated():
        return user.pk
    else:
        return ANONYMOUS

def get_obj_type_pk(obj):
    obj_type = str(obj.__class__.__name__).lower()
    
    if obj.__class__ in (User, AnonymousUser,):
        obj_pk = get_user_pk(obj)
    else:
        obj_pk = obj.pk
    
    return obj_type, obj_pk


#===============================================================================
# Stamp handling
#===============================================================================

def stamp_key(obj):
    obj_type, obj_pk = get_obj_type_pk(obj)
    return "%s-%s" % (obj_type, obj_pk)
    
def stamp_rubber(obj):
    """Invalidate the cache for the passed object.
    """
    if obj: # If the object is None, do nothing (it's pointless)
        key = stamp_key(obj)
        stamp = int(time.time())
        cache.delete(key)
        cache.set(key, stamp, CACHE_TIME)
        
        return stamp

def get_stamp(obj):
    """Returns the cached counter for the given object instance
    """
    stamp = cache.get(stamp_key(obj))
    if not stamp:
        stamp = 0
    return stamp

def rankz_key(user, obj):
    user_pk = get_user_pk(user)
    user_stamp = get_stamp(user)
    obj_type, obj_pk = get_obj_type_pk(obj)
    obj_stamp = get_stamp(obj)
    
    return "%s-%s-%s-%s-%s" % (user_pk, user_stamp,
                               obj_type, obj_pk, obj_stamp)


#===============================================================================
# Main functions
#===============================================================================

def cache_get_rankz(get_rankz):

    @wraps(get_rankz)
    def decorator(obj, user):
        key = rankz_key(user, obj)
        rankz = cache.get(key)

        if rankz is None:
            rankz = get_rankz(obj, user)
            cache.set(key, rankz, CACHE_TIME)
        return rankz
    
    return decorator
