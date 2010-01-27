# -*- coding: utf-8 -*-

from cPickle import loads, dumps
from django.db.models.fields import TextField
from copy import copy

class PickledField(TextField):
    
    """
    Поля для хранения сериализованных данных с ленивой десераилизацией.
    Сериализованное значение попадает в объект под именем <имя поля>_value.
    Статус десериализации доступен в объекте как <имя поля>_unpickled.
    """
    
    empty_strings_allowed = False
    
    def __init__(self, *args, **kwargs):
        kwargs.update(null=False, blank=False, editable=False)
        if 'default' in kwargs:
            self.default_value = copy(kwargs['default'])
        else:
            self.default_value = None
        super(PickledField, self).__init__(self, *args, **kwargs)
    
    def get_default(self):
        return self.default_value
    
    def contribute_to_class(self, cls, name):
        super(PickledField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, property(self._get_value, self._set_value))
    
    def _get_value(self, obj):
        if hasattr(obj, self.name + '_unpickled'):
            return getattr(obj, self.name  + '_value')
        else:
            value = loads(str(getattr(obj, self.name + '_value')))
            setattr(obj, self.name + '_value', value)
            setattr(obj, self.name + '_unpickled', True)
            return value
    
    def _set_value(self, obj, value):
        if not obj.pk:
            setattr(obj, self.name + '_unpickled', True)
            return setattr(obj, self.name + '_value', value)
        elif hasattr(obj, self.name + '_unpickled'):
            return setattr(obj, self.name + '_value', value)
        else:
            value = loads(str(value))
            setattr(obj, self.name + '_unpickled', True)
            return setattr(obj, self.name + '_value', value)
    
    def get_db_prep_save(self, value):
        return dumps(value)