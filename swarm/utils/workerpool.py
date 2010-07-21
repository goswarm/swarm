import threading, signal
from exceptions import IndexError

class Thread(threading.Thread):
    def __init__(self, pool):
        threading.Thread.__init__(self)
        self.pool = pool
        self.running = False
        self._queue = []
    def run(self):
        self.running = True
        while self.running:
            f, args, kwargs = self.pool.pop(0)
            try:
                f(*args, **kwargs)
            except:
                continue
    def stop(self):
        self.running = False

class Pool:
    def __init__(self, nthreads=1):
        self._queue = Queue()
        self.threads = []
        for x in range(nthreads):
            t = Thread(self)
            t.start()
            self.threads.append(t)
        signal.signal(signal.SIGINT, self.quit)
    def quit(self, signum=None, frame=None):
        def qf(): pass
        for thread in self.threads:
            thread.running = False
        for thread in self.threads:
            self.queue(qf)
    def queue(self, f, *args, **kwargs):
        self._queue.append((f, args, kwargs))
    def pop(self, i=0):
        return self._queue.pop(i)

class Queue(list):
    def __init__(self, base=[], *args, **kwargs):
        list.__init__(base, *args, **kwargs)
        self.semaphore = threading.Semaphore(0)
    def pop(self, i=0):
        self.semaphore.acquire()
        return super(Queue, self).pop(i)
    def insert(self, i, _i):
        super(Queue, self).insert(i, _i)
        self.semaphore.release()
    def append(self, _i):
        super(Queue, self).append(_i)
        self.semaphore.release()
    def __delitem__(self, i):
        self.semaphore.acquire()
        super(Queue, self).__delitem__(i)

def main():
    def test_func(a, b=2):
        print a, b
        sleep(1)
    
    p = Pool(5)
    sleep(2)
    for x in range(0,5):
        for y in range(5,10):
            p.queue(test_func, x, b=y)

if __name__ == "__main__":
    main()
