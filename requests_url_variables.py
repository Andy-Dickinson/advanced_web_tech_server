from flask import Flask, request
app = Flask(__name__)



@app.route("/")
def root():
    return "The default, 'root' route"


# A route will accept Get requests by default, and also supports HEAD automatically when GET present.
# Specify route can accept other requests using 'methods'
# use if..else to execute different code relevant to requests
@app.route("/account/", methods=['GET', 'POST'])
def account():

    # can print out request info on server for debug purposes
    print("request info:", request.form)#request.method, request.path, request.form)
    print("URL:", request.root_url)

    # to test GET request, just visit URL/account/
    # to test POST: curl -i -X POST <server_URL>:<port>/account/ -d "name=<name>"
    if request.method == 'POST':
        print (request.form)
        name = request.form['name']
        return "Hello %s" % name
    else:
        page = '''
        <html>
        <body>
            <form action="" method="post" name="form">
                <label for="name">Name:</label>
                <input type="text" name="name" id="name"/>
                <input type="submit" name="submit" id="submit"/>
            </form>
        </body>
        </html>
        '''
        return page


# route URL with variables, go to <URL>:<port>/hello/<name>
# <name> provided gets injected into <name> variable below in the route and used in the function
@app.route("/hello/<name>")
def hello(name):
    return "Hello %s" % name


# by default, URL variables are strings, but can specify other types:
# go to <url>:<port>/add/<a_number>/<another_number>
@app.route("/add/<int:first>/<int:second>")
def add(first, second):
    return str(first+second)


# URL parameters can be sent within the URL and retrieved with flask args attribute of request object
# NOTE - this is non-secure data
# visit <url>:<port>/pass_a_param/ 
# then visit <url>:<port>pass_a_param/?name=<name>
@app.route("/pass_a_param/")
def pass_a_param():
    name = request.args.get('name', '')

    if name == "":
        return "no param supplied"
    else:
        return "Hello %s" % name



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)