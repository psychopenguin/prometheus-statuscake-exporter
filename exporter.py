import os
import logging
from flask import Flask
import statuscake

logging.basicConfig(level=logging.os.environ.get('LOG_LEVEL', 'INFO'))
SERVICE_PORT = int(os.environ.get('SERVICE_PORT', 9213))
app = Flask(__name__)

@app.route('/metrics')
def metrics():
    return statuscake.get_metrics()

if __name__ == '__main__':
    statuscake.scheduler.start()
    statuscake.update_metrics()
    app.run(host="0.0.0.0", port=SERVICE_PORT, threaded=True, debug=True)
