"""
Synchronous blocking engine that processes requests one by one.
"""

import requests

from . import BaseEngine


class SyncEngine(BaseEngine):
    @staticmethod
    def create_session(**params):
        session = requests.Session()

        for param in params:
            setattr(session, param, params[param])

        return session

    def process_bulk_request(self, method, url, container, bulk_params):
        return [resource for params in bulk_params for resource in self.request(method, url, params=params)[container]]
