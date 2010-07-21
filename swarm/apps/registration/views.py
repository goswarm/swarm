"""
Views which allow users to create and activate accounts.

"""

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponseRedirect

from swarm.apps.registration.forms import AuthenticationForm
from swarm.apps.registration.forms import RegistrationForm
from swarm.apps.registration.models import RegistrationProfile
from swarm.apps.base.forms import HotSneaksErrorList

from datetime import datetime,timedelta

def activate(request, activation_key,
             template_name='registration/activate.html',
             extra_context=None):
    """
    Activate a ``User``'s account from an activation key, if their key
    is valid and hasn't expired.
    
    By default, use the template ``registration/activate.html``; to
    change this, pass the name of a template as the keyword argument
    ``template_name``.
    
    **Required arguments**
    
    ``activation_key``
       The activation key to validate and use for activating the
       ``User``.
    
    **Optional arguments**
       
    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.
    
    ``template_name``
        A custom template to use.
    
    **Context:**
    
    ``account``
        The ``User`` object corresponding to the account, if the
        activation was successful. ``False`` if the activation was not
        successful.
    
    ``expiration_days``
        The number of days for which activation keys stay valid after
        registration.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    registration/activate.html or ``template_name`` keyword argument.
    
    """
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
        
    return render_to_response(template_name,
                              { 'account': account,
                                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
                              context_instance=context)


def register(request, success_url=None,
             form_class=RegistrationForm,
             template_name='registration/registration_page.html',
             extra_context=None):
    """
    Allow a new user to register an account.
    
    Following successful registration, issue a redirect; by default,
    this will be whatever URL corresponds to the named URL pattern
    ``registration_complete``, which will be
    ``/accounts/register/complete/`` if using the included URLConf. To
    change this, point that named pattern at another URL, or pass your
    preferred URL as the keyword argument ``success_url``.
    
    By default, ``registration.forms.RegistrationForm`` will be used
    as the registration form; to change this, pass a different form
    class as the ``form_class`` keyword argument. The form class you
    specify must have a method ``save`` which will create and return
    the new ``User``.
    
    By default, use the template
    ``registration/registration_form.html``; to change this, pass the
    name of a template as the keyword argument ``template_name``.
    
    **Required arguments**
    
    None.
    
    **Optional arguments**
    
    ``form_class``
        The form class to use for registration.
    
    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.
    
    ``success_url``
        The URL to redirect to on successful registration.
    
    ``template_name``
        A custom template to use.
    
    **Context:**
    
    ``form``
        The registration form.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    registration/registration_form.html or ``template_name`` keyword
    argument.
    
    """
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect("/")

    if request.method == 'POST':
        form = form_class(data=request.POST,auto_id='am_%s')
        if form.is_valid():
            new_user = form.save()
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.
            return HttpResponseRedirect(success_url or reverse('registration_complete'))
    else:
        form = form_class(auto_id='am_%s')
    
    context = {
        'forms': {
            'registration_form': form
        }
    }

    if extra_context is None:
        extra_context = {}
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
        
    return render_to_response(template_name,context,context_instance=RequestContext(request))

def registration_complete(request):
    from django.views.generic.simple import direct_to_template
    return direct_to_template(request,'registration/registration_complete.html',context)

def login(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Displays the login form and handles the login action.
    """
     # If the user is logged in, redirect to the home page
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect("/")
       
    # Otherwise, we process the form
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationForm(request)
    request.session.set_test_cookie()
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
    }, context_instance=RequestContext(request))

login = never_cache(login)
    
def logout(request, next_page=None, template_name='registration/logged_out.html', redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    from django.contrib.auth import logout
    logout(request)
    
    context = {
        'title': _('Logged out'),
    }
    response = render_to_response(template_name, context, context_instance=RequestContext(request))    
    return HttpResponseRedirect('/')
    
def ws_login(request):
    """
    Parses and responds to a webservices login request.
    """
    from swarm.utils.wsu import return_json_response
    timer_start = datetime.now()
    context = {
        "action": "%s" % reverse("auth_ws_login"),
        "result": { "success": 0, "message": "Invalid username or password" }
    }
    user = request.user
    try:
        if user.is_authenticated():
            # Let the system know the person is already authenticated.
            context['result']['success'] = 1
            context['result']['message'] = "Already authenticated"
        else:            
            if request.method == "POST":
                form = AuthenticationForm(data=request.POST)
                if form.is_valid():
                    from django.contrib.auth import login
                    login(request, form.get_user())
                    if request.session.test_cookie_worked():
                        request.session.delete_test_cookie()
                    context['result']['success'] = 1
                    context['result']['message'] = "Logged in. Redirecting."
                else:
                    # TODO: process errors into json response
                    print form._errors
    except:
        # Admins need to know personally if there's an error happening
        subject = "Authentication Error"
        import sys, traceback
        import cStringIO
        from django.core.mail import mail_admins
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        message = "%s\n\n%s" % (request.raw_post_data, traceback.format_exc(),)
        mail_admins(subject=subject,message=message)

    timer_end = datetime.now()
    context['delta'] = timer_end - timer_start

    return return_json_response(context)

ws_login = never_cache(ws_login)


def ws_register(request):
    """
    Parses and responds to a webservices login request.
    """
    from swarm.utils.wsu import return_json_response
    timer_start = datetime.now()
    context = {
        "action": "%s" % reverse("registration_ws_register"),
        "result": { "success": 0, "message": "Not authorized" }
    }
    user = request.user
    try:
        if user.is_authenticated():
            # Let the system know the person is already authenticated.
            context['result']['success'] = 1
            context['result']['message'] = "Already authenticated"
        else:            
            if request.method == "POST":
                form = RegistrationForm(data=request.POST)
                if form.is_valid():
                    new_user = form.save()
                    from django.contrib.auth import login, authenticate
                    new_user = authenticate(username=new_user.username, password=form.cleaned_data['password1'])
                    login(request, new_user)
                    if request.session.test_cookie_worked():
                        request.session.delete_test_cookie()
                    context['result']['success'] = 1
                    context['result']['message'] = "Registered. Logged in. Redirecting."
                    utype = form.cleaned_data['user_type']
                    if utype == 'bus':
                        redirect = "/businesses/new/"
                    elif utype == 'ins':
                        redirect = "/institutions/new/"
                    elif utype == 'pro':
                        redirect = "/professionals/new/"
                    else:
                        redirect = "/"
                    context['result']['redirect'] = redirect
                else:
                    # TODO: process errors into json response
                    context['result']['message'] = "Please check for errors and try again."
                    context['result']['errors'] = form.errors
    except:
        # Admins need to know personally if there's an error happening
        subject = "Authentication Error"
        import sys, traceback
        import cStringIO
        from django.core.mail import mail_admins
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        message = "%s\n\n%s" % (request.raw_post_data, traceback.format_exc(),)
        mail_admins(subject=subject,message=message)

    timer_end = datetime.now()
    context['delta'] = timer_end - timer_start

    return return_json_response(context)