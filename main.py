from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user # anything on current user can be accessed via current_user
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from models import User, User_subscription, Club, Chat, Message, Event

db = SQLAlchemy()

app = Flask(__name__)

DB_NAME = "database.db"

app.config['SECRET_KEY'] = 'sdfsfs'  
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 

db.init_app(app) 


# creates database
# passes app configurations and checks if the app is availiable
with app.app_context():

    # checks if database exists
    if not path.exists('website/' + DB_NAME):
        db.create_all() 
        print('Createed Database!')


# initialises login manager
login_manager = LoginManager()
login_manager.login_view = 'base' # where flask should redirect if not logged in
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Load the User using SQLAlchemy's session
    return db.session.query(User).get(int(user_id))





@app.route('/')
def base():
    return render_template('base.html'), 200


@app.route('/login', methods=['POST'])
def login():
    return redirect(url_for('base'))# ---------------------------------------------------------------------


@app.route('/signup', methods=['POST'])
def signup():
    return redirect(url_for('base')) # --------------------------------------------------------------------


# check redirected if not authenticated --------------------------------------------------------------------------
@app.route('/home')
@login_required
def home():
    return render_template('home.html'), 200




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)
    # Set debug to False before submitting ---------------------------------------------------------------------------------------------------------------


