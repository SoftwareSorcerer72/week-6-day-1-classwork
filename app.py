from flask import Flask # Import the Flask Class from the Flask module


# Create an instance of Flask called app which will be the central object
app = Flask(__name__)


# Define a route
@app.route('/')
def index():
    first_name = 'Brian'
    age = 55
    return 'Hello ' +first_name + ' who is ' + str(age) + 'years old'
