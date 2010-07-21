from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'swarm.apps.base.views.about'),
    url(r'^contact/$', 'swarm.apps.base.views.contact'),
    url(r'^help/$', 'swarm.apps.base.views.help'),
    url(r'^terms/$', 'swarm.apps.base.views.tos'),
    url(r'^privacy/$', 'swarm.apps.base.views.privacy'),
    url(r'^copyright/$', 'swarm.apps.base.views.copyright'),
)

