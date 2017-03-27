import os
import logging
from flask import Flask
from prometheus_client import Gauge
from prometheus_client.exposition import generate_latest
from apscheduler.schedulers.background import BackgroundScheduler
import random

logging.basicConfig(level=logging.os.environ.get('LOG_LEVEL', 'INFO'))
SERVICE_PORT = int(os.environ.get('SERVICE_PORT', 9213))
app = Flask(__name__)
scheduler = BackgroundScheduler()

random_metric = Gauge('a_random_metric', 'random metric')

@scheduler.scheduled_job('interval', seconds=30)
def update_metrics():
    random_metric.set(random.choice(range(100)))


@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    scheduler.start()
    update_metrics()
    app.run(host="0.0.0.0", port=SERVICE_PORT, threaded=True, debug=True)
