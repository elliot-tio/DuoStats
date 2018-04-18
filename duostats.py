from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, current_app
from wtforms import Form, StringField, TextAreaField, SelectField, IntegerField, PasswordField, validators

app = Flask(__name__)

# Home


@app.route('/')
def index():
    return render_template('index.html')

# Results


@app.route('/results')
def about():
    return render_template('results.html')


# Main function - remove debug to remove dynamic update
if __name__ == '__main__':
    app.secret_key = 'duoSecret123'
    app.run(debug=True)
