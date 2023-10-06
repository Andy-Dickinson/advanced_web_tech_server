from flask import Flask, render_template, request
app = Flask(__name__)


# visit <url>:<port>/hi/<name>, name passed in URL is passed as argument to function - used with template that uses Jinja2 placeholder 'user.name'
@app.route('/hi/<name>')
def hi(name=None): # function name DOES NOT need to match route
    user = {'name':name}
    return render_template('templating_how_to/hello.html', user=user) # default render_template location is 'templates', however further subdirectories can be specified here



# multiple routes now point to this function, if a name is passed (or any other string), it will be rendered in the placeholder
@app.route('/')
@app.route('/hello/')
@app.route('/hello/<name>')
def hello_conditional(name=None): # default value set for 'name'
    return render_template('templating_how_to/conditional.html', name=name)


# list of names is passed to Jinja2 which is then looped through in the html page and each is used in the placeholder. Dictionaries can be used in a similar manner
@app.route('/users/')
def users():
    names = ['simon', 'thomas', 'lee', 'jamie', 'andy']
    return render_template('templating_how_to/looping_a_list.html', names=names)



# Inheritance ------------------------------------------
# Route to base page - it is NOT necessary to provide a route to the base page for other pages to inherit from it
@app.route('/inherits/')
def inherites():
    return render_template('templating_how_to/template_inheritance/base.html')


# first_example extends base and changes content
@app.route('/inherits/one/')
def inherits_one():
    return render_template('templating_how_to/template_inheritance/first_example.html')


# second_example also extends base, changes content in different way to first_example
@app.route('/inherits/two/')
def inherits_two():
    return render_template('templating_how_to/template_inheritance/second_example.html')

# -------------------------------------------------------


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)