# -*- coding: utf-8 -*-
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db import models

__all__ = (
    'PhoneField',
)

clean_reg = re.compile('[^\d\+]*')

class PhoneField(forms.RegexField):
    u'''
        Form field checking that phone is full (starts with "+") and normalizes
            it to only plus symbol and digits
    '''
    regex = re.compile('^\+[\d ]+\(?\d*\)?[\d -]+$')
    
    default_error_messages = {
        'required': _(u'This field is required.'),
        'invalid': _(u'Введите телефон с кодом страны и города (или мобильного '
                    u'оператора) в формате +7 (495) ххх-хх-хх или +7495ххххххх'),
    }
    
    def __init__(self, *args, **kwargs):
        self.error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            self.error_messages.update(kwargs['error_messages'])
        super(PhoneField, self).__init__(self.regex, *args, **kwargs)
    
    def clean(self, phone):
        super(PhoneField, self).clean(phone)
        return clean_reg.subn('', phone)[0]

class DBPhoneField(models.CharField):
    '''
        Form field using PhoneField as formfield and normalizing phone value
            in the same way
    '''
    
    description = _("String (up to %(max_length)s)")

    def __init__(self, *args, **kwargs):
        defaults = {'max_length': 20}
        defaults.update(kwargs)
        super(DBPhoneField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = self.to_python(value)
        if value:
            value = clean_reg.subn('', value)[0]
        return value
    
    def formfield(self, **kwargs):
        return super(DBPhoneField, self).formfield(form_class=PhoneField)
