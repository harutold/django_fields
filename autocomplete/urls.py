from django.conf.urls.defaults import *

urlpatterns = patterns('django_fields.autocomplete.views',
    (r'^(?P<name>\w+)/$', 'get_records'),
)
