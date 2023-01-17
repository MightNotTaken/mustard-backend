from flask import Flask, request, Response
import subprocess
import os
import json
import threading
import streamer

from datetime import datetime

from files_utils import get_index, add_new_entry
from export_file import ExportComponent

app = Flask(__name__)

exporter = ExportComponent()

@app.route("/")
def streamFrames():
    return Response(streamer.encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")


@app.route("/expiry", methods=["GET"])
def expiryDate():
    today = int(datetime.now().strftime("%Y%m%d"))
    try:
        with open('cx.conf', 'r') as cx:
            dt = int(cx.read())
            if dt < today:
                return {
                    "expired": True
                }, 200
        return {
            "expired": False
        }, 200
    except Exception as error:
        return {
            "expired": False
        }, 200

@app.route("/initiate-expiry")
def initiateExpiry():
    try:
        with open('cx.conf', 'w') as cx:
            cx.write('20230731')
        return {
            "status": True
        }, 200
    except Exception as error:
        print(error)
        return error, 200


@app.route("/remove-expiry", methods=['GET'])
def extendExpiryDate():
    try:
        os.unlink('cx.conf')
        return {
            "status": True
        }, 200
    except Exception as error:
        print(error)
        return error, 404

@app.route('/getNextID', methods=['GET'])
def get_next_id():
    try:
        index = get_index()
        return {'index': index}, 200
    except Exception as error:
        return str(error), 400

@app.route('/addEntry', methods=['GET'])
def add_entry():
    try:
        data = json.loads(request.args.get('data'))
        add_new_entry(data)
        return {'status': 'done'}, 200
    except Exception as error:
        print(error)
        return str(error), 400

@app.route('/export/<id>', methods=['GET'])
def export(id):
    try:
        id = int(id)
        exporter.export(id)
        return {'status': id}, 200
    except Exception as error:
        print(error)
        return {'status': 'error in exporting'}, 200

@app.route('/getTotalFiles', methods=['GET'])
def get_total_files():
    try:
        total = exporter.load()
        return {'total': total}, 200
    except Exception as error:
        print(error)
        return str(error), 400

@app.route('/shutdown', methods=['GET'])
def shutdown():
    try:
        subprocess.run(['shutdown', 'now'])
        return {'status': 'done'}, 200
    except Exception as error:
        print(error)
        return str(error), 400


def run_electron_app():
    subprocess.run(['electron', '/home/nvidia/project/mustard-seed-tester'])

def run_server():
    app.run(port=3030)




if __name__ == '__main__':

    streaming_thread = threading.Thread(target=streamer.captureFrames)
    streaming_thread.daemon = True
    streaming_thread.start()

    # electron_thread = threading.Thread(target=run_electron_app)
    # electron_thread.daemon = True
    # electron_thread.start()

    server_thread = threading.Thread(target=run_server)
    server_thread.start()
