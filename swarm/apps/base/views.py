from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def home(request):
    """
    This is the home page of the application.
    """
    from swarm.apps.registration.forms import AuthenticationForm
    from swarm.apps.registration.forms import RegistrationForm
    from swarm.apps.profiles.models import UserProfile

    user = request.user
    if user.is_authenticated():
        profile,created = UserProfile.objects.get_or_create(user=user)
        if 'amigeo' in profile.vanity_name:
            if profile.user.first_name or profile.user.last_name:
                profile.save()
        return HttpResponseRedirect("/people/%s" % profile.vanity_name)
    
    context = {
        'forms': {
            'login_form': AuthenticationForm(auto_id='am_%s'),
            'registration_form': RegistrationForm(auto_id='am_%s')
        }
    }
    return render_to_response('base/home.html', context, context_instance=RequestContext(request))

def help(request):    
    pass
    
def contact(request):
    user = request.user
    context = {}
    return render_to_response('base/contact.html', context, context_instance=RequestContext(request))

def about(request):
    user = request.user
    context = {}
    return render_to_response('base/about.html', context, context_instance=RequestContext(request))

def copyright(request):
    user = request.user
    context = {}
    return render_to_response('base/copyright.html', context, context_instance=RequestContext(request))

def report(request):
    user = request.user
    context = {}
    return render_to_response('base/report.html', context, context_instance=RequestContext(request))

def privacy(request):
    return HttpResponseRedirect("http://sites.google.com/a/swarm.com/privacy-policy/")

def tos(request):    
    return HttpResponseRedirect("http://sites.google.com/a/swarm.com/terms-of-service/")
    
def redirect(request):
    """Redirect to main screen if bad url"""
    return HttpResponseRedirect("/")
