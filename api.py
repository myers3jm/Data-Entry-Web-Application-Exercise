# Author:   Jared Myers
# Date:     08.07.2025
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class DataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    hometown = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'Data(name={self.name}, age={self.age}, title={self.title}, hometown={self.hometown})'

@app.route('/')
def home():
    return '''
    <h1>Data Entry Web Application</h1>
    <p>Created by Jared Myers, 08.07.2025</p>'''

if __name__ == '__main__':
    app.run(debug=True)