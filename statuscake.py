import os
import requests
import logging
from prometheus_client import Gauge
from prometheus_client.exposition import generate_latest

logging.basicConfig(level=logging.os.environ.get('LOG_LEVEL', 'INFO'))
SC_API_KEY = str(os.environ.get('SC_API_KEY'))
SC_USERNAME = str(os.environ.get('SC_USERNAME'))
SC_ENDPOINT = 'https://app.statuscake.com/API/'
AUTH_HEADERS = {'API': SC_API_KEY, 'Username': SC_USERNAME}

metrics = {
    'uptime': Gauge('statuscake_uptime', '7 day % uptime for this site', ['website'])
    }


def get_tests():
    req = requests.get(f'{SC_ENDPOINT}/Tests/', headers=AUTH_HEADERS)
    tests = req.json()
    for test in tests:
        metrics['uptime'].labels(website=test['WebsiteName']).set(test['Uptime'])

def update_metrics():
    get_tests()


def get_metrics():
    return generate_latest()
