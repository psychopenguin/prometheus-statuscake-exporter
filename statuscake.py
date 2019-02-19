import os
import requests
import logging
from prometheus_client import Gauge, Summary
from prometheus_client.exposition import generate_latest
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.os.environ.get('LOG_LEVEL', 'INFO'))
SC_API_KEY = str(os.environ.get('SC_API_KEY'))
SC_USERNAME = str(os.environ.get('SC_USERNAME'))
SC_ENDPOINT = 'https://app.statuscake.com/API/Tests/'
AUTH_HEADERS = {'API': SC_API_KEY, 'Username': SC_USERNAME}
scheduler = BackgroundScheduler()

baselabels = ['website', 'testid']
checklabels = ['status', 'location']
metrics = {
    'up': Gauge('statuscake_status', 'check if site is up', baselabels),
    'uptime': Gauge('statuscake_uptime', '7 day % uptime for this site', baselabels),
    'performance': Summary('statuscake_performance', 'load time in ms', baselabels + checklabels)
    }

def get_tests():
    logging.info('Retrieving tests list')
    req = requests.get(f'{SC_ENDPOINT}', headers=AUTH_HEADERS)
    logging.info(f'{req.status_code} {req.url}')
    tests = req.json()
    for test in tests:
        if test['Status'] == 'Up':
            metrics['up'].labels(test['WebsiteName'], test['TestID']).set(1)
        else:
            metrics['up'].labels(test['WebsiteName'], test['TestID']).set(0)

        metrics['uptime'].labels(test['WebsiteName'], test['TestID']).set(test['Uptime'])
    return [{'id': test['TestID'], 'name': test['WebsiteName']} for test in tests]


def get_checks(test):
    logging.info(f'Retrieving checks for {SC_ENDPOINT}')
    params={'TestID': test['id'],
            'Limit': 1,
            'Fields': 'status,location,performance'}
    req = requests.get(f'{SC_ENDPOINT}/Checks', params=params, headers=AUTH_HEADERS)
    results = req.json().popitem()[1]
    m = metrics['performance'].labels(test['name'], test['id'], results['Status'], results['Location'])
    m.observe(results['Performance'])


@scheduler.scheduled_job('interval', minutes=5)
def update_metrics():
    for test in get_tests():
        get_checks(test)


def get_metrics():
    return generate_latest()
