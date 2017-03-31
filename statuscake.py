import os
import requests
import logging
from prometheus_client import Gauge
from prometheus_client.exposition import generate_latest
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.os.environ.get('LOG_LEVEL', 'INFO'))
SC_API_KEY = str(os.environ.get('SC_API_KEY'))
SC_USERNAME = str(os.environ.get('SC_USERNAME'))
SC_ENDPOINT = 'https://app.statuscake.com/API/'
AUTH_HEADERS = {'API': SC_API_KEY, 'Username': SC_USERNAME}
scheduler = BackgroundScheduler()

labels = ['website', 'testid']
metrics = {
    'up': Gauge('statuscake_status', 'check if site is up', labels),
    'uptime': Gauge('statuscake_uptime', '7 day % uptime for this site', labels)
    }

def get_tests():
    req = requests.get(f'{SC_ENDPOINT}/Tests/', headers=AUTH_HEADERS)
    tests = req.json()
    for test in tests:
        if test['Status'] == 'Up':
            metrics['up'].labels(test['WebsiteName'], test['TestID']).set(1)
        else:
            metrics['up'].labels(test['WebsiteName'], test['TestID']).set(0)

        metrics['uptime'].labels(test['WebsiteName'], test['TestID']).set(test['Uptime'])

@scheduler.scheduled_job('interval', seconds=30)
def update_metrics():
    get_tests()


def get_metrics():
    return generate_latest()
