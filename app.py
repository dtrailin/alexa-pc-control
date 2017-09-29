from flask import Flask
from flask import abort, request
import os
import dbus
from flask import g
import time
import subprocess

app = Flask(__name__)

@app.after_request
def per_request_callbacks(response):
    for func in getattr(g, 'call_after_request', ()):
        func()
    return response

def after_this_request(func):
    if not hasattr(g, 'call_after_request'):
        g.call_after_request = []
    g.call_after_request.append(func)
    return func

@app.before_request
def limit_remote_addr():
      if request.remote_addr != '127.0.0.1':
        abort(403)  # Forbidden

@app.route('/shutdown')
def shutdown():
    @after_this_request
    def turn_off():
        print("Shutting down")
        time.sleep(2)
        sys_bus = dbus.SystemBus()
        ck_srv = sys_bus.get_object('org.freedesktop.ConsoleKit', '/org/freedesktop/ConsoleKit/Manager')
        ck_iface = dbus.Interface(ck_srv, 'org.freedesktop.ConsoleKit.Manager')
        stop_method = ck_iface.get_dbus_method("Stop")
        stop_method()
    return "True"

@app.route('/on')
def on():
    print("You're already on dummy")
    return "True"

@app.route('/netflixon')
def netflix_on():
    @after_this_request
    def do_netflix_on():
        subprocess.call("google-chrome --fullscreen http://www.netflix.com && xdotool key F11", shell=True)
        print("Opening Netflix")

    return "True"


@app.route('/netflixoff')
def netflix_off():
    @after_this_request
    def do_netflix_off():
        subprocess.call("wmctrl -c chrome", shell=True)
        print("Closing Netflix")

    return "True"
