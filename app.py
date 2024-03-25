from flask import Flask # Import the Flask Class from the Flask module


# Create an instance of Flask called app which will be the central object
app = Flask(__name__)


# Define a route
@app.route('/')
def index():
    first_name = 'Brian'
    age = 55
    return 'Hello ' +first_name + ' who is ' + str(age) + 'years old'

@app.route('/test')
def test():
    my_dicts = []
    for i in range(5):
        a_dict = {
            'id': i+1,
            'key': 'value',
            'name': 'Brian'
        }
        my_dicts.append(a_dict)

    return my_dicts
