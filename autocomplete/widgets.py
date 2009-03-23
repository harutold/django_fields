# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django_utils import flatatt

class AutocompleteWidget(forms.Widget):
    input_type = 'text'

    def __init__(self, code=None, fn=lambda v: {'success': False}, *args, **kwargs):
        super(AutocompleteWidget, self).__init__(*args, **kwargs)
        if not code:
            from uuid import uuid4
            code = uuid4().get_hex()
        self.code = code
        self.attrs={'class':'autocomplete'}
        from django_fields.autocomplete import views
        views.store[u'%s' % code] = fn        

    def render(self, name, value, attrs=None):        
        try:
            url = reverse('django_fields.autocomplete.views.get_records', args=[self.code])
        except:
            raise Exception, u'can\'t reverse autocomplete url, add it to urlconf'
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        return mark_safe(u'<input%s /><a href="%s" class="autocompleter_url"></a>' % (flatatt(final_attrs), url))

