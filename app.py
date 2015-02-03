import json
import time
import collections

from flask import Flask, render_template

# huey stuff
from config import huey
import tasks
import download_helper


app = Flask(__name__,static_folder = 'static')
app.tasks = collections.OrderedDict();

def json_response(data=None, status="ok"):
    return json.dumps({"status": status, "timestamp": time.time(), "data": data})

@app.route('/')
def index():
    return render_template('index.html', status=app.status)

@app.route('/fetch/<sceneid>')
def fetch(sceneid):
    # start the background job
    jobkey = 'fetch/'+sceneid;
    if jobkey in tasks:
        if tasks[jobkey]['ref'].get(): return json_response()
    ref = tasks.fetch(sceneid)
    task={'ref': ref, 'timestamp': time.time()};
    app.tasks.update({jobkey: task})
    job_submit(ref, "fetch", sceneid=sceneid)
    return json_response()

@app.route('/status')
def status():
    jobs = collections.OrderedDict()
    for jobkey in tasks:
        result = app.tasks[jobkey]['ref'].get()
        if result is None:
            result='Active'
        else:
            del app.tasks[jobkey]
        jobs.update({jobkey: result})
        print jobkey + ':' + result
    return json_response({"jobs": jobs, "timestamp": time.time()})


@app.route('/search/<partial>')
def search(partial):
    return json_response({"matches": download_helper.searchscenes(partial)})



if __name__ == '__main__':
    app.debug = True
    app.run()

