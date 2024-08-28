import  random
import string

from helpers.session_reset import end_user_session
from helpers.local_remote_app_actions import get_local_user_upn

from flask import Flask, render_template, request, redirect, url_for, session

APPLICATION_PORT = 5000
APPLICATION_DEBUG = False


token_for_flask_secret_key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                                     for _ in range(50))
app = Flask(__name__)
app.secret_key = token_for_flask_secret_key

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        session['email'] = email  # Store email in session
        return redirect(url_for('get_email'))
    return render_template('index.html', message=None)

@app.route('/get-email', methods=['GET'])
def get_email():
    email = session.get('email')  # Retrieve email from session
    if email == get_local_user_upn():
        processed_email = end_user_session(email)
        session.pop('email', None)  # Clear the session
        message = f"Session disconnect for: {email} successfully submitted."
        return render_template('success.html', message=message)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=APPLICATION_DEBUG, threaded=True, port=APPLICATION_PORT)
