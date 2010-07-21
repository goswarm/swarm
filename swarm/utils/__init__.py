import time, base64, urllib, hashlib, hmac, random, sys, re, traceback
from datetime import datetime

def get_exc_str():
    exc = sys.exc_info()
    exc_tb = ''.join(traceback.format_tb(exc[2]))
    exc_string = "%s: %s" % (exc[1].__class__.__name__, unicode(exc[1].message))
    return exc_string

def generateS3Url(AWS_ACCESS_KEY, AWS_SECRET_KEY, bucket, object_id, timeout = 1200):
    access_key = AWS_ACCESS_KEY
    secret_key = AWS_SECRET_KEY
    expires = time.mktime(time.localtime()) + timeout
    stringToSign = 'GET\n\n\n%d\n/%s/%s' % (expires,bucket,object_id)
    signature = urllib.quote_plus(base64.encodestring(hmac.new(secret_key,stringToSign,hashlib.sha1).digest()).strip())
    return 'http://s3.amazonaws.com/%s/%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (bucket,object_id,access_key,expires,signature)

def difftime(then, _abs=False):
    now = strptime()
    delta = now - then
    delta_secs = (delta.days*86400) + delta.seconds + (delta.microseconds/1000000.0)
    if _abs: return abs(delta_secs)
    return delta_secs

def set_path(d, v, p):
    assert type(p) in (list, tuple)
    assert type(d) in (dict, list, tuple)
    current = d
    for k in p[:-1]:
        current = current[k]
    current[p[-1]] = v

def get_path(d, p):
    assert type(p) in (list, tuple)
    assert type(d) in (dict, list, tuple)
    current = d
    for k in p[:-1]:
        current = current[k]
    return current[p[-1]]

def delete_path(d, p):
    assert type(p) in (list, tuple)
    assert type(d) in (dict, list, tuple)
    current = d
    for k in p[:-1]:
        current = current[k]
    del current[p[-1]]

def generate_object_id(length=8):
    import random
    return u''.join([random.choice('BCDFGHJKLMNPQRSTVWXYZ2345678') for i in xrange(length)])

def timeit(func, *args, **kwargs):
    t = time.time()
    result = func(*args, **kwargs)
    t = time.time()-t
    return t, 1/t, result

def slugify(value):
    # slugify from django, taken out for global use
    import unicodedata
    value = unicodedata.normalize('NFKD', unicode(value)).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

def str_to_attr(s):
    mod, attr = s.rsplit('.',1)
    mod = __import__(mod, {}, {}, [attr])
    return getattr(mod, attr)

def list_to_callables(l):
    for i in range(len(l)):
        s = l[i]
        if type(s) in (str, unicode):
            l[i] = str_to_attr(s)
