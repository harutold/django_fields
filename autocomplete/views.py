# -*- coding: utf-8 -*-

from django_utils import *

store = {}

@json
def get_records(request, name):
    try:
        v = request.POST.get('value')
        r = store[name](v)
        if type(r) is dict:
            return r
    except:
        return {'success': False}
    return {'success': True, 'items': r}