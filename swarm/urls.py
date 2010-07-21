import os
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
# from swarm.apps.gigs.models import Listing

admin.autodiscover()    

urlpatterns = patterns('',
    # Robots
    (r'^robots\.txt$', 'django.views.generic.simple.redirect_to', {'url': settings.MEDIA_URL+'robots/robots.txt'}),
    (r'^sitemap\.xml$', 'django.views.generic.simple.redirect_to', {'url': settings.MEDIA_URL+'robots/sitemap.xml'}),
        
    # Edit
    
    # Browse
    url(r'^$','swarm.apps.base.views.home',name='generic_home'),
    
    # People
    url(r'^people/(?P<vanity_name>[a-z0-9]+)/','swarm.apps.profiles.views.user_profile_detail', name='generic_profile'),

    # People
    url(r'^organizations/(?P<vanity_name>[a-z0-9]+)/','swarm.apps.profiles.views.organization_profile_detail', name='organization_profile'),
    url(r'^profiles/new/$','swarm.apps.profiles.views.create_organization_profile', name='create_organization_profile'),
    
    # static files
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_ROOT, 'static')}),
    
    # registration
    (r'^accounts/', include('swarm.apps.registration.urls')),
        
    # help, about
    (r'^about/', include('swarm.apps.base.urls')),
        
    # dummy confirmation for now
    url(r'^confirmation/$', direct_to_template, {'template': 'gigs/confirmation.html'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
	# XHR web services
	(r'^ws/', include('swarm.apps.webservice.urls')),
)

if settings.STAGE == "prod":
    urlpatterns = patterns('',
        url(r'.*', direct_to_template, { 'template': 'base/hideall.html' }),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
