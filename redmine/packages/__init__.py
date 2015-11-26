from . import requests

try:
    external_requests = __import__('requests', level=0)
except ImportError:
    pass
else:
    if requests.__build__ < external_requests.__build__:
        requests = external_requests
