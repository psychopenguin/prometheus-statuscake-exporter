import os
import logging
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import statuscake

logging.basicConfig(level=logging.os.environ.get('LOG_LEVEL', 'INFO'))
SERVICE_PORT = int(os.environ.get('SERVICE_PORT', 9213))
app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/metrics')
def metrics():
    return statuscake.get_metrics()

if __name__ == '__main__':
    scheduler.add_job(statuscake.update_metrics, 'interval', seconds=30)
    scheduler.start()
    app.run(host="0.0.0.0", port=SERVICE_PORT, threaded=True, debug=True)
