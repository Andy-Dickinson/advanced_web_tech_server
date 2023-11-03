from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from os import path
from flask_login import LoginManager
from models import db, User, User_subscription, Club, Chat, Message, Event


login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    DB_NAME = "database.db"
    db_uri = f'sqlite:///{DB_NAME}' 

    app.config['SECRET_KEY'] = 'sdfsfs'  # usually set as environment variable on desktop/environment, can get from os os.environ.get['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app) 


    # creates database
    # passes app configurations and checks if the app is availiable
    with app.app_context():
        # checks if database exists
        if not path.exists(DB_NAME):
            db.create_all() 
            print('Created Database!')

    # initialises login manager
    login_manager.login_view = 'base' # where flask should redirect if not logged in
    login_manager.init_app(app)

    return app


app = create_app()

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

@login_manager.user_loader
def load_user(user_id):
    # Load the User using SQLAlchemy's session
    return db.session.query(User).get(int(user_id))





@app.route('/')
def base():
    return render_template('base.html'), 200


@app.route('/login', methods=['POST'])
def login():

    # Get form information
    username = request.form.get('username')
    password = request.form.get('password')

    # get the first user with the matching username (if any)
    user = User.query.filter_by(username=username).first()    # old style query
    
    if user:
        if False:
        # if check_password_hash(user.password, password): # hashes provided password and checks against hashed password in database
        #     flash('Logged in successfully!', category='success')

        #     login_user(user, remember=True) # remembers user is logged in unless user clears browsing history or session or server restarts
        #     return redirect(url_for('home'))
            pass
        else:
            return jsonify({"success": False, "message": "Incorrect password, try again  SERVER SIDE "}) #---------------------------------------
    else:
        return jsonify({"success": False, "message": "User does not exist  SERVER SIDE"})  #--------------------------------------------

    




     # Validate the login data
    # if not is_valid_login(request.form):
    if True: #-----------------------------------------------------------------------------------------------------
        # Handle the validation error
        return jsonify({"success": False, "message": "Invalid login credentials"})

    # If validation is successful, redirect to the home page
    return redirect(url_for('home'))


@app.route('/signup', methods=['POST'])
def signup():
    # Validate the signup data
    # if not is_valid_signup(request.form):
    if True:  #----------------------------------------------------------------------------------------------------
        # Handle the validation error
        return jsonify({"success": False, "message": "Invalid signup data  SERVER SIDE"}) #-----------------------------------------

    # If validation is successful, redirect to the home page
    return redirect(url_for('home'))


# check redirected if not authenticated --------------------------------------------------------------------------
@app.route('/home')
@login_required
def home():
    return render_template('home.html'), 200




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)



