import os.path as path, unittest, string, random, re
__dir__ = path.dirname(path.abspath(__file__))

class Validator:
    def __init__(self):
        f = open(path.join(__dir__, "tlds.txt"))
        self.TLD_LIST = map(string.lower, f.read().split("\n"))
        f.close()
        self.IP_RE = re.compile(r'^([0-9]){1,3}.([0-9]){1,3}.([0-9]){1,3}.([0-9]){1,3}$')
    def is_email(self, s):
        allowable = set(string.ascii_letters + string.digits + ".-!#$%&'*+-/=?^_`{|}~")
        try:
            local, domain = map(string.lower, s.split("@",1))
        except: return False
        if not self.is_domain(domain) and not self.is_ip(domain): return False
        if local.startswith('.') or local.endswith('.'): return False
        if not set(local).issubset(allowable): return False
        return True
    def is_ip(self, s):
        try:
            a, b, c, d = map(int, self.IP_RE.match(s).groups())
        except: return False
        if 0<a<256 and b<256 and c<256 and 0<d<256: return True
        return False
    def is_domain(self, s):
        allowable = set(string.ascii_letters + string.digits + '-')
        if len(s) > 255: return False
        chunks = s.split(".")
        if len(chunks) < 2: return False
        if not chunks[-1].lower() in self.TLD_LIST: return False
        for x in chunks:
            if len(x) < 2: return False
            if x.startswith('-') or x.endswith('-'): return False
            if not set(x).issubset(allowable): return False
        return True

class ValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = Validator()
    def generate_email(self):
        local_valid = string.ascii_letters + string.digits +"!#$%&'*+-/=?^_`{|}~."
        local = ""
        local_length = random.randint(1,64)
    def test__is_email(self):
        emails = {
                    'aa@bb.cc':True,
                    'a@bb.cc':True,
                    'b@c.co.uk':False,
                    'abc@def.m':False
                 }
        for email, value in emails.iteritems():
            self.assertEqual(self.validator.is_email(email), value)
    def test__is_ip(self):
        ips = {
                '1.1.1.1':True,
                '1.23.123.0':False,
                '1.23.124.32':True
              }
        for ip, value in ips.iteritems():
            self.assertEqual(self.validator.is_ip(ip), value)
    def test__is_domain(self):
        domains = {
                    'bb.cc':True,
                    'b-b.cc':True,
                    'c.co.uk':False,
                    'def.m':False
                  }
        for domain, value in domains.iteritems():
            self.assertEqual(self.validator.is_domain(domain), value)

if __name__ == "__main__":
    unittest.main()
