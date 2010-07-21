from swarm.settings import *
from swarm.stages.prod import private_settings as ps

STAGE = "prod"

DEBUG = False

DATABASE_ENGINE = ps.DATABASE_ENGINE
DATABASE_NAME = ps.DATABASE_NAME
DATABASE_USER = ps.DATABASE_USER
DATABASE_PASSWORD = ps.DATABASE_PASSWORD
DATABASE_HOST = ps.DATABASE_HOST
DATABASE_PORT = ps.DATABASE_PORT

# mongodb databases
MONGODB_CORE = ps.MONGODB_CORE
