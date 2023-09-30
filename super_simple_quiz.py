from flask import Flask
app = Flask(__name__)


# Each route corresponds to a different web address

# Root route (home page)
@app.route("/")
def hello():
    return """
    <h1>A Super Simple Quiz Example</h1>
    
    <p>Hi folks.</p>
    <p>Welcome to this super simple quiz site example. It's meant to be 
    a really straightforward proof of concept that demonstrates the 
    simplest kind of onlinie quiz using just some basic Python & Pure 
    Flask (i.e. no static files or templates. Minimal HTML, CSS, & JS
    ).</p>
    
    <b>Do you want to play a game?</b>
    
    <a href="/q1/">Damn right I want to play a game!</a>
    """


@app.route("/q1/")
def q1():
    return """
    <h1>Question One</h1>
    <p>Which is the best university in Edinburgh?</p>
    
    <ul>
        <li><a href="/q2/">Edinburgh Napier</a></li>
        <li><a href="/q1w/">University of Edinburgh</a></li>
        <li><a href="/q1w/">Queen Margaret</a></li>
    <ul>
    """


# wrong answers for question 1 get routed here
@app.route("/q1w/")
def q1w():
    return """
    <h1 >Das ist der wrong answer!</h1>
    
    <a href="/q1/">Do you want to try again?</a>
    """


# correct answer to q1 routes here
@app.route("/q2/")
def q2():
    return """
    <h1>Question Two</h1>
    <p>Which is the best university in Scotland?</p>

    <ul>
        <li><a href="/q3/">Edinburgh Napier</a></li>
        <li><a href="/q2w/">University of Edinburgh</a></li>
        <li><a href="/q2w/">Herriot Watt</a></li>
        <li><a href="/q2w/">Queen Margaret</a></li>
    <ul>
    """


# wrong answers to q2 get routed here
@app.route("/q2w/")
def q2w():
    return """
    <h1>That answer was a little lacking in correctness.</h1>

    <a href="/q2/">Do you want to try again?</a>
    """


# correct answer to q2 routed here
@app.route("/q3/")
def q3():
    return """
    <h1>Question Three</h1>
    <p>Which is the best university in the UK?</p>

    <ul>
    <li><a href="/success/">Edinburgh Napier</a></li>
    <li><a href="/q3w/">University of Edinburgh</a></li>
    <li><a href="/q3w/">Herriot Watt</a></li>
    <li><a href="/q3w/">Queen Margaret</a></li>
    <ul>
    """


# incorrect answers to q3 get routed here
@app.route("/q3w/")
def q3w():
    return """
    <h1>Afraid not!</h1>
    <p>Perhaps consider whether there was a pattern forming amongst the
    answers to previous questions?</p>

    <a href="/q3/">Do you want to try again?</a>
    """


# correct answer to q3 routed here which provides link to home page
@app.route("/success/")
def success():
    return """
    <h1>You answered all the questions correctly</h1>
    <h2>Well done you</h2>

    <a href="/">Let ’s return to the home page</a>
    """


# controls how Python module and flask app server is run
if __name__ == " __main__ ":
    app.run(host=" 0.0.0.0 ")
