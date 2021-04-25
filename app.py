#!/usr/bin/python3
#
# Speedr - Internet connection speed reporting service.
#

from flask import Flask
import json
import schedule
import speedtest
import threading
import time

app = Flask(__name__)

data = {
    'download_speed': None,
    'upload_speed': None
}

running_checks = None

@app.route('/')
def speedr_summary():
    return f"""
        <html>
            <body>
                <h1>Download Speed</h1>
                <p>{data['download_speed']}</p>
                <h1>Upload Speed</h1>
                <p>{data['upload_speed']}</p>
            </body>
        </html>
    """

@app.route('/api/speed')
def speedr_api_speed():
    return json.dumps(data)

@app.route('/metrics')
def speedr_metrics():
    return f"""
        # HELP speedr_download_speed A value in bit/second of the latest measured download speed.
        # TYPE speedr_download_speed gauge
        speedr_download_speed={data["download_speed"]}
        # HELP speedr_upload_speed A value in bit/second of the latest measured upload speed.
        # TYPE speedr_upload_speed gauge
        speedr_upload_speed={data["upload_speed"]}
    """

def check_speed():
    print("Checking speed....")
    speed_test = speedtest.Speedtest()
    speed_test.get_best_server()
    speed_test.download()
    speed_test.upload()
    result = speed_test.results.dict()

    data["download_speed"] = result["download"]
    data["upload_speed"] = result["upload"]
    print(data)

def check_every_minutes(minutes):
    schedule.every(minutes).minutes.do(check_speed)

    running_checks = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not running_checks.is_set():
                schedule.run_pending()
                time.sleep(10)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return

check_speed()
check_every_minutes(5)
