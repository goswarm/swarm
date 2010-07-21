from swarm.settings import *
import os

STAGE = "dev"

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','..', 'swarm.db'))
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

# mongodb databases
MONGODB_CORE = "swarm_dev_8001"
