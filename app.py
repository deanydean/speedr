#!/usr/bin/python3
#
# Speedr - Internet connection speed reporting service.
#

from flask import Flask
import json
import os
import schedule
import speedtest
import sys
import threading
import time

app = Flask(__name__)

data = {
    'download_speed': None,
    'upload_speed': None
}

running_checks = None

check_interval = int(os.getenv('SPEEDR_CHECK_INTERVAL', 30))

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
speedr_download_speed {data["download_speed"]}
# HELP speedr_upload_speed A value in bit/second of the latest measured upload speed.
# TYPE speedr_upload_speed gauge
speedr_upload_speed {data["upload_speed"]}
    """

def check_speed():
    try:
        print("Checking speed....")
        speed_test = speedtest.Speedtest(secure=True)
        speed_test.get_best_server()
        speed_test.download()
        speed_test.upload()
        result = speed_test.results.dict()

        data["download_speed"] = int(result["download"])
        data["upload_speed"] = int(result["upload"])
        print(data)
    except:
        print("Failed to check speed: ", sys.exc_info()[0])

def schedule_checks():
    schedule.every(check_interval).minutes.do(check_speed)
    stop_running = threading.Event()

    class ScheduleThread(threading.Thread):
        def run(self):
            while not stop_running.is_set():
                schedule.run_pending()
                sleep_for = schedule.idle_seconds()
                print(f"Running next check in {sleep_for} seconds")
                time.sleep(sleep_for if sleep_for is not None else 1)

    checks_thread = ScheduleThread()
    checks_thread.start()

check_speed()
schedule_checks()
