import  random
import string

from helpers.sleeper import end_user_session_delayed

from flask_executor import Executor
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

APPLICATION_PORT = 5000
APPLICATION_DEBUG = False
APPLICATION_THREADED = True


token_for_flask_secret_key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)

                                     for _ in range(50))

app = Flask(__name__)
executor = Executor(app)
app.secret_key = token_for_flask_secret_key


@app.route('/api/upn', methods=['POST'])
def get_user_session_upn():
    global user_upn
    upn = request.form.get('upn')
    if upn:
        session['upn'] = upn
        user_upn = upn
        return jsonify({"status": "UPN received"}), 200
    return jsonify({"status": "UPN not received"}), 400


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        session['email'] = email  # Store email in session
        return redirect(url_for('get_email'))
    return render_template('index.html', user_email=user_upn)


@app.route('/get-email', methods=['GET'])
def get_email():
    email = session.get('email')  # Retrieve email from session
    if email == user_upn:
        executor.submit(end_user_session_delayed, user_upn)
        session.pop('email', None)  # Clear the session
        message = f"Session disconnect for: {email} successfully submitted."
        return render_template('success.html', message=message)
    else:
        print('User and UPN mismatch')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=APPLICATION_DEBUG, threaded=APPLICATION_THREADED, port=APPLICATION_PORT)
