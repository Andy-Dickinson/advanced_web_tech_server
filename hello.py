# imports the Flask class from the flask library
from flask import Flask, redirect, url_for, abort

# Creates an instance of the Flask class.
# __name__ is the name of flask applications module.
# Variable 'app' is used to reference the instantiated Flask class
app = Flask(__name__)


# lines beginning @ are decorators
# route() decorator here tells Flask which URL (route) should trigger the function that it decorates
# Here when browser hits root of url ('/')
@app.route('/')
def hello_world():
    return 'The default, "root" route'


# accessed via 'home_url/hello/' or 'ip:port/hello/'
@app.route("/hello/")
def hello():
    return "Hello Napier!!! :D"


@app.route("/goodbye/")
def goodbye():
    return "Goodbye cruel world :("


@app.route("/private")
def private():
    # Test for user logged in failed
    # so redirect to login URL
    return redirect(url_for('login'))  # url for login


@app.route('/login')
def login():
    return "Now we would get username & password"


@app.route('/force404')
def force404():
    abort(404)  # causes an error (the one passed), useful for testing and injecting errors


# redirection for when page not found (404 status code)
@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't find the page you requested.", 404  # 404 here returns the code to the browser (see console)


# can retrieve static files
@app.route('/static-example/img')
def static_example_img():
    start = '<img src="'
    # note sub folder must be specified under filename. 'static' is the default directory flask looks in
    url = url_for('static', filename='/img/vmask.jpg')
    end = '">'
    return start+url+end, 200


if __name__ == "__main__":
    print("test if __name__ == '__main__' in hello.py")
    app.run(host='0.0.0.0', debug=True)
