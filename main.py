# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import time
from flask import Flask, render_template, request


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')
    # return "G'day GAE st. 101"


@app.route('/latency')
def latency():
    "Adding some latency"
    latency = request.args.get('latency')
    latency = int(latency) if latency else 150
    time.sleep(latency)
    return "{}sec latency".format(latency)


@app.route('/memory')
def use_memory():
    memory = request.args.get('memory')
    memory = int(memory) if memory else 128
    tmp = bytearray(int(memory)*1000000)

    latency = request.args.get('latency')
    if latency:
        time.sleep(int(latency))
        return '{}MB memory was allocated for {}sec'.format_map(memory, latency)

    return '{}MB memory was allocated.'.format_map(memory)


@app.route('/cpu')
def fib():
    n = request.args.get('n')
    n = int(n) if n else 10000

    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        
    return 'fib({}) = {}'.format(n, b)


@app.route('/500')
def server_error():
    return 1/0


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
