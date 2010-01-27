

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminFileWidget
from django.core.files import File
from os.path import join
from django.conf import settings

class DeleteCheckboxWidget(forms.CheckboxInput):
    def __init__(self, *args, **kwargs):
        self.show_delete = kwargs.pop('show_delete')
        super(DeleteCheckboxWidget, self).__init__(*args, **kwargs)
    def render(self, name, value, attrs=None):
        if self.show_delete:
            return u'<label for="%s" style="margin-left:9em;">%s %s</label>' % (attrs['id'], super(DeleteCheckboxWidget, self).render(name, value, attrs), _('Delete'))
        else:
            return u''

class RemovableFileFormWidget(forms.MultiWidget):
    def __init__(self, show_delete=False, admin=True):
        if admin:
            Cl = AdminFileWidget
        else:
            Cl = forms.FileInput
        widgets = (Cl(), DeleteCheckboxWidget(show_delete=show_delete))
        super(RemovableFileFormWidget, self).__init__(widgets)
        
    def decompress(self, value):
        return [value, None]

class RemovableFileFormField(forms.MultiValueField):
    widget = RemovableFileFormWidget
    field = forms.FileField
    
    def __init__(self, inst, key, admin=True, *args, **kwargs):
        self.inst=inst
        self.key=key
        self.model_field = getattr(self.inst, self.key)
        fields = [self.field(*args, **kwargs), forms.BooleanField(required=False)]
        show_delete = False
        if self.model_field:
            show_delete = True
        self.widget = self.widget(show_delete=show_delete, admin=admin)
        super(RemovableFileFormField, self).__init__(fields, required=False)
        
    def compress(self, data_list):
        return data_list[0]
        
    def clean(self, value):
        if value[1]:
            try:
                self.model_field.delete()
            except IOError:
                f = open(join(settings.CURDIR, "media", self.model_field.name), "w")
                self.model_field.delete()
        return super(RemovableFileFormField, self).clean(value)

__all__ = ('RemovableFileFormField', )
