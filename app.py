import  random
import string

from helpers.sleeper import end_user_session_delayed
from helpers.user_state import unique_token, add_to_user_state, remove_user_from_state, get_user_upn_from_state, get_user_token_from_state, show_all_user_states


from flask_executor import Executor
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

# TODO to env vars or config file
APPLICATION_PORT = 5000
APPLICATION_DEBUG = False
APPLICATION_THREADED = True
DUMMY_EMAIL_ADDRESS = 'your_email_address@here.org'


app = Flask(__name__)
executor = Executor(app)
app.secret_key = unique_token(length=50)


@app.route('/api/upn', methods=['POST'])
def get_user_session_upn():
    """

    :return:
    """
    upn = request.form.get('upn')
    if upn:
        session['upn'] = upn
        add_to_user_state(upn)
        return jsonify({"status": "UPN received"}), 200
    return jsonify({"status": "UPN not received"}), 400


@app.route('/', methods=['GET', 'POST'])
def index():
    """

    :return:
    """
    if request.method == 'POST':
        email = request.form['email']
        session['email'] = email
        return redirect(url_for('get_email'))
    return render_template('index.html', user_email=DUMMY_EMAIL_ADDRESS)


@app.route('/get-email', methods=['GET'])
def get_email():
    """

    :return:
    """
    email = session.get('email').lower()
    # print(show_all_user_states())
    if email == get_user_upn_from_state(email) and get_user_token_from_state(email):
        executor.submit(end_user_session_delayed, get_user_upn_from_state(email))
        remove_user_from_state(email)
        session.pop('email', None)  # Clear the session
        message = f"Session disconnect for: {email} successfully submitted."
        return render_template('success.html', message=message)
    else:
        print('User and UPN mismatch')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=APPLICATION_DEBUG, threaded=APPLICATION_THREADED, port=APPLICATION_PORT)
