import os

from . import requests

try:
    external_requests = __import__('requests', level=0)
except ImportError:
    pass
else:
    if os.getenv('REDMINE_USE_EXTERNAL_REQUESTS') or requests.__build__ < external_requests.__build__:
        requests = external_requests
