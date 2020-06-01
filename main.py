from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from retrying import retry
from tasks import run

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("SuperSecurePassword")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None

@app.route('/')
@auth.login_required
def hello():
    return render_template('index.html')

@app.route("/start", methods=["GET", "POST"])
@auth.login_required
@retry(retry_on_result=retry_if_result_none, stop_max_attempt_number=2)
def start():
    if request.method == "GET":
        output = run.start_time_entry()
        return output
    else:
        return "Not Found", 404

@app.route("/stop", methods=["GET", "POST"])
@auth.login_required
@retry(retry_on_result=retry_if_result_none, stop_max_attempt_number=2)
def stop():
    if request.method == "GET":
        output = run.stop_time_entry()
        return output
    else:
        return "Not Found", 404


if __name__ == '__main__':
    """
    This is used when running locally only. When deploying to Google App
    Engine, a webserver process such as Gunicorn will serve the app. This
    can be configured by adding an `entrypoint` to app.yaml.
    """
    app.run(host='127.0.0.1', port=8080, debug=True)