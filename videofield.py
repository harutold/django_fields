import re

from django import forms
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'VideoField',
)

VIDEO = {
      'rutube.ru': ((u'''<OBJECT width="320" height="265">
                    <PARAM name="movie" value="''','''"></PARAM>
                    <PARAM name="wmode" value="window"></PARAM><PARAM name="allowFullScreen" value="true"></PARAM>
                    <EMBED src="http://video.rutube.ru/''','''" type="application/x-shockwave-flash" wmode="window" width="320" height="265" allowFullScreen="true" ></EMBED>
                    </OBJECT>'''), re.compile('(?:\?|&)v=([\w-]+)')),
      'youtube.com': ((u'''<object width="320" height="265">
                    <param name="movie" value="http://www.youtube.com/v/''','''&hl=en&fs=1&rel=0&color1=0x2b405b&color2=0x6b8ab6"></param>
                    <param name="allowFullScreen" value="true"></param>
                    <param name="allowscriptaccess" value="always"></param>
                    <embed src="http://www.youtube.com/v/''','''&hl=en&fs=1&rel=0&color1=0x2b405b&color2=0x6b8ab6" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="320" height="265"></embed>
                    </object>'''), re.compile('(?:\?|&)v=([\w-]+)')),
        'smotri.com': ((u'''<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" width="320" height="265">
                    <param name="movie" value="http://pics.smotri.com/scrubber_custom8.swf?file=''',
'''&bufferTime=3&autoStart=false&str_lang=rus&xmlsource=http%3A%2F%2Fpics.smotri.com%2Fcskins%2Fblue%2Fskin_color_lightaqua.xml&xmldatasource=http%3A%2F%2Fpics.smotri.com%2Fskin_ng.xml" /><param name="allowScriptAccess" value="always" /><param name="allowFullScreen" value="true" /><param name="bgcolor" value="#ffffff" /><embed src="http://pics.smotri.com/scrubber_custom8.swf?file=''', '''&bufferTime=3&autoStart=false&str_lang=rus&xmlsource=http%3A%2F%2Fpics.smotri.com%2Fcskins%2Fblue%2Fskin_color_lightaqua.xml&xmldatasource=http%3A%2F%2Fpics.smotri.com%2Fskin_ng.xml" quality="high" allowscriptaccess="always" allowfullscreen="true" wmode="window"  width="400" height="330" type="application/x-shockwave-flash"></embed></object>'''),
                    re.compile('(?:\?|&)id=([\w-]+)')),
    }
VIDEO_REG = re.compile('http://(?:www\.)?('+ '|'.join(VIDEO.keys()) +')/(.*)')

class VideoField(forms.URLField):
    
    default_error_messages = {
        'required': _(u'This field is required.'),
        'not_valid': _(u'This video url is not valid.'),
    }
    
    def __init__(self, *args, **kwargs):
        self.error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            self.error_messages.update(kwargs['error_messages'])
        super(VideoField, self).__init__(*args, **kwargs)
    
    def clean(self, url):
        c = super(VideoField, self).clean(url)
        v = VIDEO_REG.match(url)
        if v is not None: 
            site, url = v.groups()
            if site in VIDEO:
                s, r = VIDEO[site]
                target = r.search(url)
                if target is not None:
                    x = target.groups()
                    #raise target.groups()
                    return target.groups()[0].join(s)
        raise forms.ValidationError(self.error_messages['not_valid'])
