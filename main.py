from flask import Flask, send_from_directory, render_template, session, request, redirect, \
    url_for, abort, request, jsonify, g
from flask.ext.json import json_response, FlaskJSON
import logging
import sys
import sqlite3 as sql

from utils import common

logger = logging.getLogger(__name__)
app = Flask(__name__, static_url_path='/static')

# App Configuration
app.config['JSON_ADD_STATUS'] = False
app.config['JSON_DATETIME_FORMAT'] = '%d/%m/%Y %H:%M:%S'


# Routes.....
@app.route("/addComment", methods=['POST'])
def addComment():
    parsed_json = common.parse_form_json(request.form)
    try:
        con = sql.connect("database/feedback.db")
        cur = con.cursor()
        cur.execute("INSERT INTO comments (name,email,phone,message) VALUES (?,?,?,?)",
                    (parsed_json['name'], parsed_json['email'], parsed_json['phone_number'], parsed_json['message']))
        con.commit()
        con.close()
        return json_response(statusCode=200, status=True)
    except Exception as error:
        logger.info(error)
        return json_response(statusCode=500, status=False)


@app.route("/comments")
def comments():
    try:
        con = sql.connect("database/feedback.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM comments")
        rows = cur.fetchall()
        con.close()
    except Exception as error:
        logger.info(error)
        rows = dict()

    return render_template('comments.html', comments=rows)


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            port = int(sys.argv[1])
        else:
            port = 8000
        logger.info("Starting Web Application")
        app.secret_key = '8823EB36C2F8C82C935D3195E52BD'
        app.config['SESSION_TYPE'] = 'filesystem'
        app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
    except Exception as error:
        print("Could not parse command line: [{0}]".format(error))
        print("Expected usage: [python webserver_runner.py <PORT>")
