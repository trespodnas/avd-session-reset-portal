from session_reset import end_user_avd_session
from flask import Flask, render_template, request, redirect, url_for, session


# from email_processor import process_email  # Import your function

app = Flask(__name__)
app.secret_key = 'DNT5XgwYsnHZFLG3brvVp8RJQedqjf9myBEuCAPt7WcKM6S24z'

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
    processed_email = end_user_avd_session(email)
    return f"Email retrieved: {processed_email}"

if __name__ == '__main__':
    app.run(debug=True)
