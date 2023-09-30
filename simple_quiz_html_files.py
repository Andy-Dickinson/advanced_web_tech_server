from flask import Flask, render_template

app = Flask(__name__)


# similar to super simple quiz app, but html pages now stored separately
# render_template() function is used to send html file back to caller


@app.route("/")
def hello():
    return render_template('quiz_html_files/index.html')


@app.route("/q1/")
def q1():
    return render_template('quiz_html_files/q1.html')


@app.route("/q1w/")
def q1w():
    return render_template('quiz_html_files/q1w.html')


@app.route("/q2/")
def q2():
    return render_template('quiz_html_files/q2.html')


@app.route("/q2w/")
def q2w():
    return render_template('quiz_html_files/q2w.html')


@app.route("/q3/")
def q3():
    return render_template('quiz_html_files/q3.html')


@app.route("/q3w/")
def q3w():
    return render_template('quiz_html_files/q3w.html')


@app.route("/success/")
def success():
    return render_template('quiz_html_files/success.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
