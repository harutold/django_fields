# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.forms import *
from django.utils.simplejson import dumps, loads
from widgets import *

__all__ = ('JSONField', 'TableField')

class JSONField(MultiValueField):
    
    def compress(self, data_list):
        if data_list:
            return dumps(data_list)
        return None

class TableField(JSONField):
    """
    recom_r_widgets = [TextInput() for x in range(3)]
    class RecommedationsField(JSONField):
        
        def __init__(self, *args, **kwargs):
            errors = self.default_error_messages.copy()
            if 'error_messages' in kwargs:
                errors.update(kwargs['error_messages'])
            fields = (
                CharField(max_length=200),
                CharField(max_length=200),
                CharField(max_length=200),
            )
            self.field_names=(_(u'Ф.И.О'), _(u'Компания (предприятие)'), _(u'Телефон'))
            super(RecommedationsField, self).__init__(fields, *args, **kwargs)
    """

    def __init__(self, RowField, widgets, rows=1, *args, **kwargs):
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        field_names=None
        if hasattr(RowField, 'field_names'):
            field_names=RowField.field_names
        self.widget = JSONWidgetTable([JSONWidgetTableRow(widgets) for x in range(rows)], field_names=field_names)
        fields = [RowField for x in range(rows)]
        super(TableField, self).__init__(fields, *args, **kwargs)
