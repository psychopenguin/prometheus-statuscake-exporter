import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import random

SERVICE_PORT = int(os.environ.get('SERVICE_PORT', 9213))
app = Flask(__name__)
scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', seconds=30)
def update_metrics():
    global latest_metrics
    latest_metrics = random.choice(range(100))


@app.route('/metrics')
def metrics():
    return str(latest_metrics)

if __name__ == '__main__':
    update_metrics()
    scheduler.start()
    app.run(host="0.0.0.0", port=SERVICE_PORT, threaded=True)
