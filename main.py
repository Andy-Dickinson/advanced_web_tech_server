from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from os import path
from models import db, User, User_subscription, Club, Chat, Message, Event
import bcrypt
from datetime import date
import re


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


@login_manager.user_loader
def load_user(user_id):
    # Load the User using SQLAlchemy's session
    return db.session.query(User).get(int(user_id))

# @login_manager.request_loader
# def load_user_from_request(request):
#     if request.endpoint != 'base':
#         if not current_user.is_authenticated:
#             flash("Please log in to access this page", category="error")
#             return None

#     # Return the user if they are logged in
#     return current_user



        

# unauthenticated home page
@app.route('/')
def base():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    home_link_url = '#page-top'
    return render_template('base.html', home_link_url=home_link_url), 200


# logged in home page
@app.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user), 200


# logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base'))


# login route from modal form
@app.route('/login', methods=['POST'])
def login():

    # Get form data
    username = request.form.get('username')
    password = request.form.get('password')

    # get the first user with the matching username (if any)
    user = User.query.filter_by(username=username).first()    # old style query
    
    if user:
        stored_pw = user.password
        if stored_pw == bcrypt.hashpw(password.encode('utf-8'), stored_pw):

            login_user(user, remember=True)

            flash('Logged in!', category='success')
            
            # If validation is successful, redirect to the home page
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "message": "Incorrect password, try again"}), 400
    else:
        return jsonify({"success": False, "message": "User does not exist"}), 404


# signup route from modal form
@app.route('/signup', methods=['POST'])
def signup():

    # Get form data
    username = request.form.get('username').strip()
    first_name = request.form.get('first_name')
    surname = request.form.get('surname')
    hc = request.form.get('handicap')
    email = request.form.get('email').strip()
    password = request.form.get('password').strip()
    password2 = request.form.get('password2').strip()

    # Validate the input data
    if username:  
        validated = validate_input(username, 'username')
        if (validated != ''):
            return jsonify({"success": False, "message": validated}), 400
    else:
        return jsonify({"success": False, "message": "Username required"}), 400
    
    if first_name:
        validated = validate_input(first_name, 'first_name')
        if (validated != ''):
            return jsonify({"success": False, "message": validated}), 400
        
    if surname:
        validated = validate_input(surname, 'surname')
        if (validated != ''):
            return jsonify({"success": False, "message": validated}), 400
        
    if hc:
        validated = validate_input(hc, 'handicap')
        if (validated != ''):
            return jsonify({"success": False, "message": validated}), 400
        
    if email:
        validated = validate_input(email, 'email')
        if (validated != ''):
            return jsonify({"success": False, "message": validated}), 400
    else:
        return jsonify({"success": False, "message": "Email required"}), 400
        
    if password:
        validated = validate_input(password, 'password')
        if (validated != ''):
            return jsonify({"success": False, "message": validated}), 400
    else:
        return jsonify({"success": False, "message": "Password required"}), 400
    
    if password2:
        validated = validate_input([password, password2], 'password2')
        if (validated != ''):
            return jsonify({"success": False, "message": validated}), 400
    else:
        return jsonify({"success": False, "message": "Confirm password"}), 400
    

    # Validate against database
    db_user = User.query.filter_by(username=username).first()
    if db_user:
        return jsonify({"success": False, "message": "Username already exists"}), 409
    
    db_email = User.query.filter_by(email=email).first()
    if db_email:
        return jsonify({"success": False, "message": "Email already associated with an account"}), 409

    
    # Signup user and login
    hash_salt_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, first_name=first_name, surname=surname, handicap_index=hc, email=email, password=hash_salt_pw)

    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user, remember=True)
    
    flash('Account created!', category='success')
    
    # If validation is successful, redirect to the home page
    return jsonify({"success": True}), 201


# Find games route
@app.route('/find_game', methods=['GET', 'POST'])
@login_required
def find_game():
    home_link_url = '/home'
    current_date = date.today()
    
    if request.method == 'GET':
        return render_template('find_game.html', home_link_url=home_link_url, current_date=current_date), 200
    
    if request.method == 'POST':
        return None, 201
    
    return None, 405


# update handicap
@app.route('/update_hc', methods=['GET', 'POST'])
@login_required
def update_hc():

    if request.method == 'GET':
        current_hc = current_user.handicap_index
        if current_hc:
            return jsonify({"success":True, "hc":current_hc}), 200
        else:
            return jsonify({"success":False, "hc":"None currently set"}), 200
    
    if request.method == 'POST':
        new_hc = request.form.get('handicap')

        if new_hc:
            validated = validate_input(new_hc, 'handicap')
            if (validated != ''):
                return jsonify({"success": False, "message": validated}), 400
        else:
            return jsonify({"success": False, "message": "Please enter a handicap index"}), 400
        
        # adds new handicap index to database if validated ok
        current_user.handicap_index = new_hc
        db.session.commit()

        return jsonify({"success": True, "hc": new_hc}), 201
        
    return None, 405


# Returns list of all approved clubs in database
@app.route('/all_approved_clubs')
@login_required
def all_approved_clubs():
    approved_clubs = Club.query.filter_by(approved=True).all()
    
    # Convert Club objects to dictionaries
    clubs_data = []
    for club in approved_clubs:
        club_dict = {
            "id": club.club_id,
            "name": club.club_name,
            "url": club.club_url,
            "address": club.club_address,
            "postcode": club.club_postcode,
            "phone": club.club_phone_number,
            "approved": club.approved,
            "subscriptions": [sub.user_id for sub in club.subscriptions],
            "events": [event.event_id for event in club.events], 
        }
        clubs_data.append(club_dict)
    
    return jsonify(clubs_data), 200


# Gets users current subscriptions or subscribes user as per clubs sent
@app.route('/user_subs', methods=['GET', 'POST'])
@login_required
def user_subs():
    if request.method == 'GET':
        user_subs = current_user.subscriptions

        # Convert subscription objects to dictionaries
        user_subs_data = []
        for sub in user_subs:
            sub_dict = {
                "subscription_id": sub.subscription_id,
                "user_id": sub.user_id,
                "club_id": sub.club_id,
            }
            user_subs_data.append(sub_dict)

        return jsonify(user_subs_data), 200
    
    elif request.method == 'POST':
        subed_list = request.get_json()['selectedClubs']
        
        # Get list of all approved clubs
        approved_clubs = Club.query.filter_by(approved=True).all()

        # Dictionary to map club names to IDs
        club_name_to_id = {club.club_name: club.club_id for club in approved_clubs}
        
        # Checks if any clubs in subed_list are not in approved list
        for club_name in subed_list:
            if club_name not in club_name_to_id:
                return jsonify({"success": False, "message": f"Club '{club_name}' is not an approved club"}), 400
        
        # Current user's subscriptions club ids list
        current_user_subs = [sub.club_id for sub in current_user.subscriptions]

        # Subscribe user to clubs they are not already subscribed to
        clubs_to_subscribe = [club_name_to_id[club_name] for club_name in subed_list if club_name_to_id[club_name] not in current_user_subs]
        for club_id in clubs_to_subscribe:
            club = Club.query.get(club_id)
            if club:
                user_subscription = User_subscription(user=current_user, club=club)
                db.session.add(user_subscription)
        
        # Unsubscribe user from clubs not in subed_list which currently subscribed to
        clubs_to_unsubscribe = [club_id for club_id in current_user_subs if club_id not in [club_name_to_id[name] for name in subed_list]]
        
        for club_id in clubs_to_unsubscribe:
            user_subscription = User_subscription.query.filter_by(user_id=current_user.user_id, club_id=club_id).first()
            if user_subscription:
                db.session.delete(user_subscription)
        
        db.session.commit()
        
        return jsonify({"success": True, "message": "Subscriptions updated successfully"}), 200
    
    return None, 405


# Returns list of all open events in database
@app.route('/open_events')
@login_required
def open_events():
    # Get open events which are not at full capacity
    events = Event.query.filter(Event.event_open == True, and_(Event.current_participants < Event.max_capacity)).all()
    
    # Convert event objects to dictionaries
    events_data = []
    for event in events:
        event_dict = {
            "id": event.event_id,
            "creator": event.user_id_creator,
            "club_id": event.club_id,
            "event_name": event.event_name,
            "description": event.event_description,
            "planned_date": event.datetime_as_iso(),
            "max_capacity": event.max_capacity,
            "min_hc": event.min_hc,
            "max_hc": event.max_hc,
            "current_participants": event.current_participants,
            "tee_time_booked": event.tee_time_booked, 
        }
        events_data.append(event_dict)
    
    return jsonify(events_data), 200


# Test routes ----------------------------------------------------------------------------------------------------------------------------------------
@app.route('/clear_session', methods=['GET'])
def clear_session():
    session.clear()
    return redirect(url_for('base'))

@app.route('/clear_request_data')
def clear_request_data():
    request.args = {} 
    request.form = {}
    request.cookies = {}  
    request.headers = {}  
    request.data = b'' 

    return "Request data cleared.", 200


@app.route('/add_clubs')
def add_clubs():
    db.session.query(Club).delete()
    db.session.commit()
    db.session.query(User_subscription).delete()
    db.session.commit()

    club = Club(club_name="Pumpherston", club_url="https://www.pumpherstongolfclub.co.uk/", club_address="Drumshoreland Road, Pumpherston", club_postcode="EH53 0LQ", club_phone_number="01506 433337", approved=True)

    db.session.add(club)
    db.session.commit()

    club = Club(club_name="Duddingston", club_url="https://www.duddingstongolfclub.co.uk/", club_address="Duddingston Golf Club, Duddingston Road West, Edinburgh", club_postcode="EH15 3QD", club_phone_number="0131 661 4301", approved=True)

    db.session.add(club)
    db.session.commit()

    return redirect(url_for('base'))





def validate_input(formData, field):
    if field == 'username':
        user_format = r"^[a-zA-Z0-9]+$"
        
        if len(formData) < 4:
            return 'Too short. (Minimum 4 characters)'
        elif len(formData) > 25:
            return 'Too long. (Maximum 25 characters)'
        elif not re.match(user_format, formData):
            return 'Invalid username. (Use only letters and numbers)'
    
    elif field == 'password':
        password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9\s])[^s]{8,}$"
        if len(formData) < 8:
            return 'Too short. (Minimum 8 characters)'
        elif not re.match(password_pattern, formData):
            return 'Invalid password. (Must contain at least one uppercase letter, lowercase letter, digit and special character)'
    
    elif field == 'password2':
        if formData[0] != formData[1]:
            return 'Passwords do not match'
    
    elif field in ['first_name', 'surname']:
        name_format = r"^[a-zA-Z-' ]+$"
        field = ' '.join(word.capitalize() for word in field.split('_'))
        
        if len(formData) > 100:
            return 'Too long. (Maximum 100 characters)'
        elif not re.match(name_format, formData):
            return 'Invalid ' + field + '. (Use only letters, hyphens, and spaces)'
    
    elif field == 'handicap':
        hc_pattern = r"^(?:(?:\+(?:[0-9](?:\.[0-9])?|10(?:\.0)?)|0(?:\.[0-9])?)|(?:[0-9](?:\.[0-9])?)|(?:[0-4][0-9](?:\.[0-9])?)|(?:[5][0-3](?:\.[0-9])?)|(?:[5][4](?:\.[0])?))$"
        
        if not re.match(hc_pattern, formData):
            return 'Invalid handicap. (Enter a valid handicap index, e.g., +1.5, 15, 25.4)'
    
    elif field == 'email':
        email_pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
        
        if len(formData) > 255:
            return 'Too long. (Maximum 255 characters)'
        elif not re.match(email_pattern, formData):
            return 'Invalid email. (Enter a valid email address)'
    
    return ''  # Validation passed








if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)



