from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'UserEmailField', 'UserUsernameField', 'PasswordConfirmWidget',
    'PasswordConfirmField',
)

EMPTY_VALUES = (None, '')

class UserEmailField(forms.EmailField):
    
    default_error_messages = {
        'required': _(u'This field is required.'),
        'not_unique': _(u'This email address already exists.'),
    }
    
    def __init__(self, *args, **kwargs):
        self.error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            self.error_messages.update(kwargs['error_messages'])
        super(UserEmailField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        c = super(UserEmailField, self).clean(value)
        try:
            User.objects.get(email=c)
            raise forms.ValidationError, self.error_messages['not_unique']
        except ObjectDoesNotExist:
            pass
        return c

class UserUsernameField(forms.RegexField):

    default_error_messages = {
        'required': _(u'This field is required.'),
        'not_unique': _(u'This username address already exists.'),
    }

    def __init__(self, regex='.*', *args, **kwargs):
        self.error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            self.error_messages.update(kwargs['error_messages'])
        super(UserUsernameField, self).__init__(regex=regex, *args, **kwargs)

    def clean(self, value):
        c = super(UserUsernameField, self).clean(value)
        try:
            User.objects.get(username=c)
            raise forms.ValidationError, self.error_messages['not_unique']
        except ObjectDoesNotExist:
            pass
        return c


class PasswordConfirmWidget(forms.widgets.MultiWidget):

    def __init__(self, attrs=None):
        widgets = (forms.widgets.PasswordInput(attrs=attrs), forms.widgets.PasswordInput(attrs=attrs))
        super(PasswordConfirmWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        return [value, value]

class PasswordConfirmField(forms.MultiValueField):
    
    default_error_messages = {
        'not_match': _(u'Passwords don\'t match.'),
        'required': _(u'This field is required.'),
    }
    
    def __init__(self, *args, **kwargs):
        self.error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            self.error_messages.update(kwargs['error_messages'])
        fields = (
            forms.CharField(max_length=50),
            forms.CharField(max_length=50)
        )
        super(PasswordConfirmField, self).__init__(fields, widget=PasswordConfirmWidget(), *args, **kwargs)

    def compress(self, data_list):
        for i in data_list:
            if i in EMPTY_VALUES:
                raise forms.ValidationError, self.error_messages['required']
        if data_list[0] != data_list[1]:
            raise forms.ValidationError, self.error_messages['not_match']
        return data_list[0]