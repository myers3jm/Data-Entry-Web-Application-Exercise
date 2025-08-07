# Author:   Jared Myers
# Date:     08.07.2025
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

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
    name = request.form['name']
    age = request.form['age']
    title = request.form['title']
    hometown = request.form['hometown']

    data = DataModel(name=name, age=age, title=title, hometown=hometown)
    db.session.add(data)
    db.session.commit()

    return redirect('/data/')

@app.route('/data/')
def view_data():
    return render_template('data.html', data=DataModel.query.all())

# Main program
if __name__ == '__main__':
    app.run(debug=True)