# -*- coding: utf-8 -*-

from django.forms import *
from django.utils.simplejson import dumps, loads
from django.utils.translation import string_concat

__all__ = ('JSONWidget', 'JSONWidgetTableRow', 'JSONWidgetTable')
class JSONWidget (MultiWidget):
    def __init__(self, widgets, attrs=None):
        super(JSONWidget, self).__init__(widgets, attrs)
        
    def decompress (self, value):
        if value:
            return loads(value)
        return [None for x in range(4)]

class JSONWidgetTableRow (JSONWidget):
    def format_output(self, rendered_widgets):
        return '<td>'+u'</td><td>'.join(rendered_widgets)+'</td>'

class JSONWidgetTable (JSONWidget):
    def __init__(self, widgets, attrs=None, field_names=[]):
        self.field_names=field_names
        super(JSONWidgetTable, self).__init__(widgets, attrs)
        
    def format_output(self, rendered_widgets):
        html ='<table>'
        from django.utils.encoding import force_unicode
        if self.field_names :
            html+='<tr><th>'+'</th><th>'.join([force_unicode(s) for s in self.field_names])+'</th></tr>'
        return html+'<tr>'+u'</tr><tr>'.join(rendered_widgets)+'</tr></table>'
