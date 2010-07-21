import sys
from time import *
from datetime import datetime

def strftime(t=None):
    if not t: t = datetime.utcnow()
    if sys.version_info[1] >= 6:
        return t.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def strptime(t=None):
    if not t: t = strftime()
    if sys.version_info[1] >= 6:
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")

def ago(d, now=None, res=4):
    if type(d) in (str, unicode):
        d = strptime(d)
    if not now:
        now = datetime.utcnow()
    delta = now - d
    
    t = []

    years = delta.days / 365
    days = delta.days - (years * 365)
    hours = delta.seconds / 3600
    minutes = (delta.seconds - (hours * 3600)) / 60
    seconds = delta.seconds - (minutes * 60)

    if years:
        t += ['%i years' % years]
    if days:
        t += ['%i days' % days]
    if hours:
        t += ['%i hours' % hours]
    if minutes:
        t += ['%i minutes' % minutes]
    if seconds:
        t += ['%i seconds' % seconds]

    return ', '.join(t[:res])

def until(d, now=None, res=4):
    if not now:
        now = datetime.utcnow()
    until = ago(now, d, res)
    if until.startswith('-'):
        return 'pending'
    return until
