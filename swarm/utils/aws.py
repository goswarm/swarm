import settings, jsontools, utils, logging
from boto.sqs.connection import SQSConnection
from boto.sqs.message import Message

class Queue:
    def __init__(self, AWS_ACCESS_KEY=settings.AWS_ACCESS_KEY,
                       AWS_SECRET_KEY=settings.AWS_SECRET_KEY,
                       QUEUE=settings.QUEUE):
        self.sqs_conn = SQSConnection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
#        self.queue = None
        self.queuename = "http://queue.amazonaws.com/%s" %QUEUE
        self.logger = logging.getLogger()
#    def initConnection(self):
#        self.queue = self.sqs_conn.get_queue(self.queuename)
#        if not self.queue:
#            self.queue = self.sqs_conn.create_queue(self.queuename)
    def _write(self, d):
#        if not self.queue:
#            self.initConnection()
        d['timestamp'] = utils.strftime()
        m = Message()
        p = jsontools.dumps(d)
        m.set_body(p)
        self.logger.debug("writing to aws: %s" % p)
        return self.sqs_conn.get_status('SendMessage', { "MessageBody": m.get_body_encoded() }, self.queuename)
    def traffic_hit(self, info):
        p = { "method":"traffic.hit", "args":{ "info":info } }
        self._write(p)
    def imagizer_resize(self, image_id):
        p = { "method":"imagizer.resize", "args":{ "image_id":image_id } }
        self._write(p)
    def content_create(self, content_id):
        p = { "method":"content.create", "args":{ "content_id":content_id } }
        self._write(p)
    def content_update(self, content_id):
        p = { "method":"content.update", "args":{ "content_id":content_id } }
        self._write(p)
    def content_delete(self, content_id):
        p = { "method":"content.delete", "args":{ "content_id":content_id } }
        self._write(p)
    def sdb_write(self, domain, key, data):
        p = { "method":"sdb.write", "args": {
                  "domain":domain, "key":key, "data":data
               } }
        self._write(p)
