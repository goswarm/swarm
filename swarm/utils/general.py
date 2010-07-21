import sys, traceback
from django.core.mail import mail_admins

def send_exception_email(request, subject):
    subject = "%s: %s" % (request.current_brandable.name, subject)
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    message =  "Site: %s\n\n%s" % (request.current_brandable.name, traceback.format_exc(),)
    mail_admins(subject=subject,message=message)

def clean_to_root_url(url):
	return re.sub(r'http(s)?\:\/\/|www(\d)?\.','',url).split('/')[0]