#!bin/python

from flask import Flask, request
import tasks

app = Flask(__name__)

@app.route("/statistics", methods=["GET"])
def get_statistics():
    return "blub"

@app.route("/translate", methods=["POST"])
def submit_job():
    result = tasks.translate.delay(request.form["text"], request.form["language"])
    return str(result.wait())

if __name__ == '__main__':
    app.run(debug=True)
