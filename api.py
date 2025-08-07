# Author:   Jared Myers
# Date:     08.07.2025
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from contextlib import suppress

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Error reporting class
class Error():
    msgs = []

    def __repr__(self):
        return self.msgs

# Model of how data should be stored in the database
class DataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    hometown = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'Data(name={self.name}, age={self.age}, title={self.title}, hometown={self.hometown})'

# Web interface routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit/', methods=['POST'])
def submit_form():
    # Backend input validation
    keys = ['name', 'age', 'title', 'hometown']
    name, age, title, hometown = '', '', '', ''
    if any([k not in request.form.keys() for k in keys]):
        pass
    else:
        name = request.form['name']
        age = request.form['age']
        title = request.form['title']
        hometown = request.form['hometown']

    if len(name) == 0:
        Error.msgs.append('Invalid name provided. Acceptable values are nonzero-length strings.')
    try:
        if int(age) > 150 or int(age) < 1:
            Error.msgs.append('Invalid age supplied. Acceptable values are whole numbers 1-150 inclusive.')
    except: # Provided value is not a number
        Error.msgs.append('Non-numeric age supplied. Acceptable values are whole numbers 1-150 inclusive.')
    if title not in ['Other', 'Ms.', 'Mrs.', 'Mr.', 'Dr.']:
        Error.msgs.append('Invalid title provided. Acceptable values are provided in the dropdown in the data entry form.')
    
    if len(Error.msgs) > 0:
        return redirect('/error/')

    # Write to database, validation complete

    data = DataModel(name=name, age=age, title=title, hometown=hometown)
    db.session.add(data)
    db.session.commit()

    return redirect('/data/')

@app.route('/data/')
def view_data():
    return render_template('data.html', data=DataModel.query.all())

@app.route('/error/')
def error():
    msgs = Error.msgs
    if len(msgs) == 0:
        msgs = ['Sample error']
    Error.msgs = []
    return render_template('error.html', errors=msgs)

# Main program
if __name__ == '__main__':
    app.run(debug=True)