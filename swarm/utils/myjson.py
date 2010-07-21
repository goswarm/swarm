import datetime
from swarm.utils import mytime
from exceptions import ImportError

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json

class DTEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) is datetime.datetime:
            return { "__datetime__":True, "value":mytime.strftime(obj) }
        if type(obj) is datetime.timedelta:
            return { "__timedelta__":True, "value":[obj.days, obj.seconds, obj.microseconds] }
        return super(DTEncoder, self).default(obj)

def dt_loader(dct):
    if '__datetime__' in  dct:
        return mytime.strptime(dct['value'])
    if '__timedelta__' in dct:
        return datetime.timedelta(*dct['value'])
    return dct

def dumps(o):
    enc = DTEncoder()
    return enc.encode(o)

def loads(s):
    return json.loads(s, object_hook=dt_loader)

if __name__ == "__main__":
    d = dumps(datetime.datetime.now())
    print d
    print loads(d)
    
    d = dumps(datetime.timedelta(7903, 15832, 554343))
    print d
    print loads(d)
