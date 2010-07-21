from django.forms.util import ErrorList
from django.utils.safestring import mark_safe

class HotSneaksErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return mark_safe(u'<div class="ui-state-error ui-corner-all ly_error" style="padding: 0pt 0.7em;">%s</div>' % ''.join([u'<p>%s</p>' % e for e in self]))

class TextErrorList(ErrorList):
    def __unicode__(self):
        return self.as_text()
    def as_text(self):
        if not self: return u''
        return mark_safe(u'%s' % ''.join([u'%s' % e for e in self]))