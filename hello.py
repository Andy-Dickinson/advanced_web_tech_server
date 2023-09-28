from flask import Flask # imports the Flask class from the flask library
app = Flask(__name__) # Creates an instance of the Flask class. __name__ is the name of flask applications module. Variable 'app' is used to reference the instantiated Flask class

@app.route('/') # lines beginning @ are decorators, route() decorator here tells Flask which URL should trigger the function that it decorates. Here when browser hits root of url ('/')
def hello_world(): 
    return 'Hello Napier'
