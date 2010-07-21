from threading import Lock

class InstDescriptor(object):
    def __init__(self, pool, attr):
        self.pool = pool
        self.attr = attr
    def __get__(self, obj, objtype):
        if not hasattr(obj, self.attr):
            setattr(obj, self.attr, self.pool.get())
        return getattr(obj, self.attr)

class Pool:
    def __init__(self, cls, min_size, max_size=10, init_args=[], init_kwargs={}):
        self.cls, self.init_args, self.init_kwargs = cls, init_args, init_kwargs
        self.min_size = min_size
        self.max_size = max_size
        self.pool = []
        self.lock = Lock()
        self.init_pool()
    def init_pool(self):
        for x in range(0, self.min_size):
            inst = self.cls(*self.init_args, **self.init_kwargs)
            self.add(inst)
    def add(self, inst):
        self.lock.acquire()
        self.pool += [inst]
        self.lock.release()
    def get(self):
        self.lock.acquire()
        if not self.pool:
            inst = self.cls(*self.init_args, **self.init_kwargs)
        else:
            inst = self.pool.pop()
        self.lock.release()
        return inst
