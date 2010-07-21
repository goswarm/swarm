from django.conf import settings
from django.core.files.storage import Storage
import boto, os, hashlib, mimetypes

def generate_object_id(length=8):
    import random
    return u''.join([random.choice('BCDFGHJKLMNPQRSTVWXYZ2345678') for i in xrange(length)])

class S3Storage(Storage):
    def __init__(self, bucket=settings.AWS_BUCKET, prefix=settings.AWS_PREFIX):
        self.s3conn = boto.connect_s3(settings.AWS_ACCESS_KEY,
                                      settings.AWS_SECRET_KEY)
        self.bucket = self.s3conn.get_bucket(bucket)
        self.prefix = prefix
    def _get_key(self, path, create=False):
        if not path.startswith(self.prefix):
            path = os.path.join(self.prefix, path)
        k = self.bucket.lookup(path)
        if not k and create:
            k = self.bucket.new_key(path)
        return k

    def exists(self, path):
        return bool(self._get_key(path))

    def path(self, path):
        return self.url(path)

    def size(self, path):
        k = self._get_key(path)
        return k.size

    def url(self, path):
#       print 'url for ', path
        k = self._get_key(path)
#       print k
        return k.generate_url(3600)

    def open(self, path, mode='rb'):
        raise NotImplementedError

    def save(self, path, content):
#       print "saving?"
        content = content.read()
        hasher = hashlib.sha1()
        hasher.update(content)
        hash = hasher.hexdigest()
        fn = hash + os.path.splitext(path)[1]
#       print "fn: ", fn
        k = self._get_key(fn, create=True)
        content_type = max(mimetypes.guess_type(k.name))
        if content_type:
            k.content_type = content_type
        k.set_contents_from_string(content)
#       print "kn: ", k.name
        return k.name

    def delete(self, path):
        k = self._get_key(path)
        k.delete()
