import json
from flask import Flask, Response, make_response, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.contrib.cache import SimpleCache

server = Flask(__name__)
auth = HTTPBasicAuth()
cache = SimpleCache()


@auth.get_password
@server.route("/")
@server.route("/about")
def about():
    return render_template('about.html')

