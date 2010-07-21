import os, sys

os.environ['PYTHON_EGG_CACHE'] = '/var/lib/deployments/eggs'

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'core', 'lib', 'python')))
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'dependencies')))

f = open("/var/log/local/swarm.stdout.staging.log", 'w')
sys.stdout = f

f = open("/var/log/local/swarm.stderr.staging.log", 'w')
sys.stderr = f

os.environ['DJANGO_SETTINGS_MODULE'] = 'swarm.stages.staging.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
