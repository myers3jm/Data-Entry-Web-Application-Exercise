# Author:   Jared Myers
# Date:     08.07.2025
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, abort

NAME_HELP_TEXT = 'Invalid name provided. Acceptable values are nonzero-length strings.'
AGE_HELP_TEXT = 'Invalid age provided. Acceptable values are whole numbers 1-150 inclusive. This field can also be left blank.'
TITLE_HELP_TEXT = 'Invalid title provided. Acceptable values are nonzero-length strings.'
HOMETOWN_HELP_TEXT = 'Acceptable values are nonzero-length strings.'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

# Error reporting class
class Error():
    msgs = []

    def __repr__(self):
        return self.msgs

# Model of how data should be stored in the database
class DataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(80), nullable=False)
    hometown = db.Column(db.String(80), nullable=False)

    # Validation method - called before making database modifications
    def validate(self) -> bool:
        # Validate name
        if self.name == None or len(self.name) == 0:
            Error.msgs.append(NAME_HELP_TEXT)
        # Validate age
        if self.age == None or self.age == '':
            self.age = None # Allow empty ages and remaining age checks
        else:
            try:
                if int(self.age) > 150 or int(self.age) < 1:
                    Error.msgs.append(AGE_HELP_TEXT)
            except: # Provided value is not a number
                Error.msgs.append(AGE_HELP_TEXT)
        # Validate title
        if self.title == None:
            Error.msgs.append(TITLE_HELP_TEXT)
        
        if len(Error.msgs) > 0:
            return False

        # Title-case validated data before returning
        self.name = self.name.title()
        self.title = self.title.title()
        self.hometown = self.hometown.title()
        return True

    def __repr__(self):
        return f'Data(name={self.name}, age={self.age}, title={self.title}, hometown={self.hometown})'

# Web interface routes
@app.route('/') # Web entry of data
def home():
    return render_template('index.html')

# Web submission of data
@app.route('/submit/', methods=['POST'])
def submit_form():
    # Gather data from request
    keys = ['name', 'age', 'title', 'hometown']
    name, age, title, hometown = '', '', '', ''
    if any([k not in request.form.keys() for k in keys]):
        pass
    else:
        name = request.form['name']
        age = request.form['age']
        title = request.form['title']
        hometown = request.form['hometown']
    
    data = DataModel(name=name, age=age, title=title, hometown=hometown)

    # Validate data before making any database modifications
    if not data.validate():
        return redirect('/error/')

    # Write to database, validation complete

    db.session.add(data)
    db.session.commit()

    return redirect('/data/')

# Web view of data
@app.route('/data/')
def view_data():
    return render_template('data.html', data=DataModel.query.all())

# Web view of errors
@app.route('/error/')
def error():
    msgs = Error.msgs
    if len(msgs) == 0:
        msgs = ['Sample error']
    Error.msgs = []
    return render_template('error.html', errors=msgs)

# API
data_args = reqparse.RequestParser() # Define args for request parser
data_args.add_argument('name', type=str)
data_args.add_argument('age', type=int)
data_args.add_argument('title', type=str)
data_args.add_argument('hometown', type=str)

# Define shape of data for marshalling
data_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'age':fields.Integer,
    'title':fields.String,
    'hometown':fields.String
}

# API submission of data
class Submit(Resource):
    def post(self):
        args = data_args.parse_args()
        data = DataModel(name=args['name'], age=args['age'], title=args['title'], hometown=args['hometown'])
        if not data.validate():
            msgs = Error.msgs
            Error.msgs = []
            return {"errors": msgs}, 400
        db.session.add(data)
        db.session.commit()
        return marshal(DataModel.query.all(), data_fields), 201
api.add_resource(Submit, '/api/submit/')

# API view of data
class Data(Resource):
    @marshal_with(data_fields)
    def get(self):
        return DataModel.query.all()
api.add_resource(Data, '/api/data/')

# Main program
if __name__ == '__main__':
    app.run(debug=True)