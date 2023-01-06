from flask import Flask, request, Response
import subprocess
import json

import threading
import streamer

from files_utils import get_index, add_new_entry
from export_file import ExportComponent

app = Flask(__name__)

exporter = ExportComponent()

@app.route("/")
def streamFrames():
    return Response(streamer.encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")


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





if __name__ == '__main__':

    streaming_thread = threading.Thread(target=streamer.captureFrames)
    streaming_thread.daemon = True
    streaming_thread.start()
    
    subprocess.run(['electron', '/home/nvidia/project/mustard-seed-tester'])

    app.run(port=3030)