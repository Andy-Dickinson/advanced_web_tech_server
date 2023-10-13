# Adding data into a session, query that data, and remove that data
# Flask provides an interface for using 'secured cookies' or sessions from our Python code and we can consider a session to be a small data store for keys and values. 
# However, note the content of a cookie can easily be read by the client or whilst it is transmitted (unless the communication has been secured with HTTPS)

'''
    # Set key=value, name=andy into a session
    session['name'] = andy

    # retrieve the value set in the session
    # This key might not exist so needs to be wrapped in a try-except
    try:
        if(session['name']):
            return str(session['name'])
    except KeyError:
        pass

    # remove a specified key and associated value from the session
    session.pop('name', None)
'''


from flask import Flask, session


app = Flask(__name__)

# Sessions rely on cookies that are cryptographically secured by Flask using a secret key to ensure that the content of the cookies hasn’t been altered by any process other than the Flask app that created it. However, the content of a cookie can easily be read 
# The secret key should really be stored either in a config file or typed in by hand at startup, but NEVER put in the code repository!
# can use 'os.urandom(24)' to generate a random key which can then be copied and pasted
app.secret_key = 'A0Zr98j /3 yX R~XHH!jmN]LWX / ,? RT'


@app.route('/')
def index():
    return "Root route for the sessions example"


# adds name passed in url to session
@app.route('/session/write/<name>/')
def write(name=None):
    session['name'] = name
    return "Wrote %s into 'name' key of session" % name


# attempts to read name in session
@app.route('/session/read/')
def read():
    try:
        if(session['name']):
            return str(session['name'])
    except KeyError:
        pass
    return "No session variable set for 'name' key"


# removes name from session
@app.route('/session/remove/')
def remove():
    session.pop('name', None)
    return "Removed key 'name' from session"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)