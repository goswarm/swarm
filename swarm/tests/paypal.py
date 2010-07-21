#!/usr/bin/python2.5
import sys
sys.stderr = sys.stdout
import os
from decimal import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
os.environ['DJANGO_SETTINGS_MODULE']="gigsly.settings"
from swarm.apps.payments.models import PaypalSenderAccount, PaypalReceiverAccount, PaypalAdaptivePayment
from swarm.apps.gigs.models import Gig
from django.contrib.auth.models import User

# Good receiver
def test_good_receiver():
	sender = PaypalSenderAccount(user=User.objects.get(id=1),paypal_email='barbie_1252622407_per@hiredly.com')
	sender.save()
	ppcp = PaypalAdaptivePayment(sender=sender,amount=Decimal("55.99"), gig=Gig.objects.get(id=1))
	try:
		receiver = PaypalReceiverAccount.objects.get(name="Noam Chomsky", paypal_email='barto_1253940759_per@hiredly.com')
	except PaypalReceiverAccount.DoesNotExist:
		receiver = PaypalReceiverAccount(name="Noam Chomsky", paypal_email='barto_1253940759_per@hiredly.com')
		receiver.save()
		
	ppcp.receiver = receiver
	
	ppcp.pay()

# Bad Receiver
def test_bad_receiver():
	sender = PaypalSenderAccount(user=User.objects.get(id=1),paypal_email='barbie_1252622407_per@hiredly.com')
	sender.save()
	ppcp = PaypalAdaptivePayment(sender=sender,amount=Decimal("55.99"), gig=Gig.objects.get(id=1))
	try:
		receiver = PaypalReceiverAccount.objects.get(name="Noam Chomsky", paypal_email='badrecevier@hiredly.com')
	except PaypalReceiverAccount.DoesNotExist:
		receiver = PaypalReceiverAccount(name="Noam Chomsky", paypal_email='badrecevier@hiredly.com')
		receiver.save()
		
	ppcp.receiver = receiver
	
	ppcp.pay()
	
# Bad Sender
def test_bad_sender():
	sender = PaypalSenderAccount(user=User.objects.get(id=1),paypal_email='badsender@hiredly.com')
	sender.save()
	ppcp = PaypalAdaptivePayment(sender=sender,amount=Decimal("55.99"), gig=Gig.objects.get(id=1))
	try:
		receiver = PaypalReceiverAccount.objects.get(name="Noam Chomsky", paypal_email='barto_1253940759_per@hiredly.com')
	except PaypalReceiverAccount.DoesNotExist:
		receiver = PaypalReceiverAccount(name="Noam Chomsky", paypal_email='barto_1253940759_per@hiredly.com')
		receiver.save()
		
	ppcp.receiver = receiver
	
	ppcp.pay()

# Bad Sender AND Bad Receiver
def test_bad_sender_and_receiver():
	sender = PaypalSenderAccount(user=User.objects.get(id=1),paypal_email='badsender@hiredly.com')
	sender.save()
	ppcp = PaypalAdaptivePayment(sender=sender,amount=Decimal("55.99"), gig=Gig.objects.get(id=1))
	try:
		receiver = PaypalReceiverAccount.objects.get(name="Noam Chomsky", paypal_email='badreceiver@hiredly.com')
	except PaypalReceiverAccount.DoesNotExist:
		receiver = PaypalReceiverAccount(name="Noam Chomsky", paypal_email='badreceiver@hiredly.com')
		receiver.save()
		
	ppcp.receiver = receiver
	
	ppcp.pay()
