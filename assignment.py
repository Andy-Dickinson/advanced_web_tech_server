from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from sqlalchemy import and_
from os import path
from models import db, User, User_subscription, Club, Chat, Message, Event
import bcrypt
from datetime import datetime
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
#             return ''

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


# login route called from modal form
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


# signup route called from modal form
@app.route('/signup', methods=['POST'])
def signup():
    try:
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
    
    except Exception as e:
        db.session.rollback()

        print("Signup failed, rolled back, error: " + str(e))

        return jsonify({"success": False, "message": "Something went wrong, signup failed, please try again later."}), 500


# Find game route
@app.route('/find_game')
@login_required
def find_game():
    home_link_url = '/home'
    current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M")

    return render_template('find_game.html', user=current_user, home_link_url=home_link_url, current_datetime=current_datetime), 200



# update handicap
@app.route('/update_hc', methods=['GET', 'POST'])
@login_required
def update_hc():

    try:
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
            
        return 'Method not allowed', 405
    
    except Exception as e:
        db.sessionn.rollback()

        print("Updating of handicap failed, rolled back, error: " + str(e))

        return jsonify({"success": False, "message": "Something went wrong, updating of handicap failed, please try again later."}), 500
        


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
    try:
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
            # List of club names user wants to subscribe to
            subed_list = request.get_json()['selectedClubs']
            
            # Get list of all approved clubs
            approved_clubs = Club.query.filter_by(approved=True).all()

            # Dictionary to map club names to IDs
            approved_club_name_to_id = {club.club_name: club.club_id for club in approved_clubs}
            
            # Checks if any clubs in subed_list are not in approved list
            for club_name in subed_list:
                if club_name not in approved_club_name_to_id:
                    # In theory should never trigger as user should only have access to select approved clubs
                    return jsonify({"success": False, "message": f"Club '{club_name}' is not an approved club"}), 400
            
            # Current user's current subscriptions club ids list
            current_user_subs = [sub.club_id for sub in current_user.subscriptions]
            
            # Subscribe user to clubs they are not already subscribed to
            clubs_to_subscribe = [approved_club_name_to_id[club_name] for club_name in subed_list if approved_club_name_to_id[club_name] not in current_user_subs]
            for club_id in clubs_to_subscribe:
                club = Club.query.get(club_id)
                if club:
                    user_subscription = User_subscription(user_id=current_user.user_id, club_id=club.club_id)
                    db.session.add(user_subscription)
            
            # Unsubscribe user from clubs not in subed_list which currently subscribed to
            clubs_to_unsubscribe = [club_id for club_id in current_user_subs if club_id not in [approved_club_name_to_id[name] for name in subed_list]]
            
            for club_id in clubs_to_unsubscribe:
                user_subscription = User_subscription.query.filter_by(user_id=current_user.user_id, club_id=club_id).first()
                if user_subscription:
                    db.session.delete(user_subscription)
            
            db.session.commit()
            
            return jsonify({"success": True, "message": "Subscriptions updated successfully"}), 201
        
        return 'Method not allowed', 405
    
    except Exception as e:
        db.sessionn.rollback()

        print("Updating subscriptions failed, rolled back, error: " + str(e))

        return jsonify({"success": False, "message": "Something went wrong, updating subscriptions failed, please try again later."}), 500


# Returns list of all open events not at capacity in database
@app.route('/open_events')
@login_required
def open_events():

    # Get open events which are not at max capacity
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
            "planned_date": event.planned_datetime,
            "max_capacity": event.max_capacity,
            "min_hc": event.min_hc,
            "max_hc": event.max_hc,
            "current_participants": event.current_participants,
            "tee_time_booked": event.tee_time_booked, 
        }
        events_data.append(event_dict)
    
    return jsonify(events_data), 200


'''
Adds user to chat they click on an event in find_game
Validation checks done prior to adding
Redirection occurs in find_game_function handleChatLinkClick if successfully added to chat
'''
@app.route('/add_user_chat', methods=['POST'])
@login_required
def add_user_chat():
    
    event_id = int(request.args.get('event_id'))

    event = Event.query.filter_by(event_id=event_id).first()

    # Validation checks encase database has been updated
    if not event:
        return jsonify({'message': "Sorry, this event has been deleted!"}), 404

    if event.current_participants >= event.max_capacity:
        return jsonify({'message': "Sorry, this event is now at full capacity"}), 409
    
    if not event.event_open:
        return jsonify({'message': "Sorry, this event is now closed!"}), 403
    
    if event.min_hc or event.max_hc:
        hc = current_user.handicap_index

        if not hc:
            return jsonify({'message': "You need a handicap to join this event!"}), 409
        
        if hc.startswith('+'):
            hc = '-' + hc[1:]
        hc_f = float(hc)
        
        if event.min_hc:
            min_hc_s = event.min_hc
            if min_hc_s.startswith('+'):
                min_hc_s = '-' + event.min_hc[1:]
            min_hc_f = float(min_hc_s)

            if hc_f < min_hc_f:
                return jsonify({'message': "Handicap too low for event!"}), 409
            
        if event.max_hc:
            max_hc_s = event.max_hc
            if max_hc_s.startswith('+'):
                max_hc_s = '-' + event.max_hc[1:]
            max_hc_f = float(max_hc_s)

            if hc_f > max_hc_f:
                return jsonify({'message': "Handicap too high for event!"}), 409

    chat = Chat.query.filter_by(event_id=event.event_id, user_id=current_user.user_id).first()
    
    if chat:
        return jsonify({'message': "You are already signed up to this event!"}), 409


    # Adds user to chat
    new_chat = Chat(
        user_id=current_user.user_id,
        event_id=event.event_id
    )

    db.session.add(new_chat)
    db.session.commit()

    new_message = Message(
        event_id=event.event_id,
        user_id=current_user.user_id,
        message=current_user.username + " joined the chat."
    )

    # Add the message to the database
    db.session.add(new_message)
    db.session.commit()

    flash("Joined event!", category='success')

    return jsonify({'route':'my_game_chats?load_chat=' + str(new_chat.event_id)})


'''
Chat page to display all users chats and messages
Optional parameter load_chat (chat_id) to load a specific chat
'''
@app.route('/my_game_chats', methods=['GET', 'POST'])
@login_required
def my_game_chats():
    
    if request.method == 'GET':
        
        # Event id to load if passed in request
        event_id = request.args.get('load_chat')
        if event_id:
            event_id = int(event_id)

        home_link_url = '/home'
        
        # All chats which user is a member
        users_chats = Chat.query.filter_by(user_id=current_user.user_id).all()
        
        # User information
        users_in_chats = {}

        # Get all users in chats
        for chat in users_chats:
            for message in chat.messages:
                # Get user's
                user_id = message.user_id
                user_username = User.query.get(user_id).username

                # Adds users to dictionary
                users_in_chats[user_id] = user_username
        
        try:
            return render_template('my_game_chats.html', user=current_user, home_link_url=home_link_url, load_chat=event_id, users_chats=users_chats, chat_users=users_in_chats), 200
        except Exception as e:
            print(f"Error rendering template: {e}")
    
    if request.method == 'POST':
        
        # POST used for adding messages to db

        return '', 200
    
    return 'Method not allowed', 405


'''
Testing routes ----------------------------------------------------------------------------------------------------------------------------------------
Setup to easily add and remove data along with clearing session and request_data from address bar. 
For production, these routes should be replaced with proper POST / DELETE routes and only called by admin or from dedicated forms.
Routes:
    * clear_session
    * clear_request_data
    * print_tables
    * add_events
    * delete_events
    * add_one_club
    * add_multi_clubs
    * delete_clubs
'''
@app.route('/clear_session')
def clear_session():
    session.clear()

    flash("Session cleared!", category="success")

    return redirect(url_for('base'))

@app.route('/clear_request_data')
def clear_request_data():
    request.args = {} 
    request.form = {}
    request.cookies = {}  
    request.headers = {}  
    request.data = b'' 

    flash("Request data cleared!", category="success")

    return redirect(url_for('base'))


@app.route('/print_tables')
def print_tables():
    
    print("\n\n")
    print("\nUser table after deleting:", User.query.all())
    print("\nClub table after deleting:", Club.query.all())
    print("\nSubscriptions table after deleting:", User_subscription.query.all())
    print("\nEvents table:", Event.query.all())
    print("\nChat table:", Chat.query.all())
    print("\nMessage table:", Message.query.all())
    print("\n\n")

    return redirect(url_for('base'))


@app.route('/add_events')
def add_events():
    try:
        # Isolates session
        with app.app_context():

            event1 = Event(
                user_id_creator=current_user.user_id,
                club_id=1,
                event_name="Putt around",
                event_description="Layed back 18 holes",
                planned_datetime=datetime.fromisoformat("2023-12-23T12:00"),  # must be date object, this should work when using data sent to server from datetime selectors
                max_capacity=4,
                current_participants=1,
                tee_time_booked=False,
                event_open=True,
            )

            db.session.add(event1)
            db.session.commit()

            chat1 = Chat(
                user_id=current_user.user_id,
                event_id=event1.event_id
            )

            db.session.add(chat1)
            db.session.commit()

            message1 = Message(
                event_id=chat1.event_id,
                user_id=current_user.user_id,
                message=current_user.username + " created the event."
            )

            db.session.add(message1)
            db.session.commit()

            event2 = Event(
                user_id_creator=current_user.user_id,
                club_id=5,
                event_name="Comp",
                event_description="Wanting to get a group together for a semi serious competition",
                planned_datetime = datetime.fromisoformat("2024-01-03T09:30"),  # must be date object, this should work when using data sent to server from datetime selectors
                max_capacity=20,
                max_hc="28.0",
                current_participants=1,
                tee_time_booked=False,
                event_open=True,
            )
            db.session.add(event2)
            db.session.commit()
            
            chat2 = Chat(
                user_id=current_user.user_id,
                event_id=event2.event_id
            )
            db.session.add(chat2)
            db.session.commit()

            message2 = Message(
                event_id=chat2.event_id,
                user_id=current_user.user_id,
                message=current_user.username + " created the event."
            )

            db.session.add(message2)
            db.session.commit()

            event3 = Event(
                user_id_creator=current_user.user_id,
                club_id=2,
                event_name="9 hole friendly",
                event_description="Looking to get a few holes played with someone from club",
                planned_datetime = datetime.fromisoformat("2024-01-10T10:30"),  # must be date object, this should work when using data sent to server from datetime selectors
                max_capacity=2,
                min_hc="15.0",
                max_hc="28.0",
                current_participants=1,
                tee_time_booked=False,
                event_open=True,
            )
            db.session.add(event3)
            db.session.commit()
            
            chat3 = Chat(
                user_id=current_user.user_id,
                event_id=event3.event_id
            )
            db.session.add(chat3)
            db.session.commit()

            message3 = Message(
                event_id=chat3.event_id,
                user_id=current_user.user_id,
                message=current_user.username + " created the event."
            )

            db.session.add(message3)
            db.session.commit()

            event4 = Event(
                user_id_creator=current_user.user_id,
                club_id=6,
                planned_datetime = datetime.fromisoformat("2024-01-05T09:00"),  # must be date object, this should work when using data sent to server from datetime selectors
                max_capacity=4,
                min_hc="+2.0",
                current_participants=1,
                tee_time_booked=False,
                event_open=True,
            )
            db.session.add(event4)
            db.session.commit()
            
            chat4 = Chat(
                user_id=current_user.user_id,
                event_id=event4.event_id
            )
            db.session.add(chat4)
            db.session.commit()

            message4 = Message(
                event_id=chat4.event_id,
                user_id=current_user.user_id,
                message=current_user.username + " created the event."
            )

            db.session.add(message4)
            db.session.commit()

            event5 = Event(
                user_id_creator=current_user.user_id,
                club_id=2,
                event_name="Sunday afternoon",
                planned_datetime = datetime.fromisoformat("2023-12-30T14:15"),  # must be date object, this should work when using data sent to server from datetime selectors
                max_capacity=2,
                min_hc="5.0",
                current_participants=1,
                tee_time_booked=False,
                event_open=True,
            )
            db.session.add(event5)
            db.session.commit()
            
            chat5 = Chat(
                user_id=current_user.user_id,
                event_id=event5.event_id
            )
            db.session.add(chat5)
            db.session.commit()

            message5 = Message(
                event_id=chat5.event_id,
                user_id=current_user.user_id,
                message=current_user.username + " created the event."
            )

            db.session.add(message5)
            db.session.commit()

            event6 = Event(
                user_id_creator=current_user.user_id,
                club_id=2,
                event_name="Foursomes",
                event_description="Fancy a foursomes xmas eve?",
                planned_datetime = datetime.fromisoformat("2023-12-24T10:00"),  # must be date object, this should work when using data sent to server from datetime selectors
                max_capacity=4,
                min_hc="+3.0",
                max_hc="54.0",
                current_participants=1,
                tee_time_booked=False,
                event_open=True,
            )
            db.session.add(event6)
            db.session.commit()
            
            chat6 = Chat(
                user_id=current_user.user_id,
                event_id=event6.event_id
            )
            db.session.add(chat6)
            db.session.commit()

            message6 = Message(
                event_id=chat6.event_id,
                user_id=current_user.user_id,
                message=current_user.username + " created the event."
            )

            db.session.add(message6)
            db.session.commit()

        flash('Events added!', category='success')

        return redirect(url_for('base'))

    except Exception as e:
        db.session.rollback()

        print("Error adding events: " + str(e))
        flash('Events not added, rolled back.', category='error')

        return redirect(url_for('base'))
    

@app.route('/delete_events')
def delete_events():
    try:
        # Isoloates session
        with app.app_context():
            events = Event.query.all()
            
            for event in events:
                chats = Chat.query.filter_by(event_id=event.event_id).all()

                for chat in chats:
                    # Delete all messages associated with the chat
                    Message.query.filter_by(event_id=chat.event_id).delete()
                
                # Delete chats associated with the event
                Chat.query.filter_by(event_id=event.event_id).delete()

                # Commit before deleteing event
                db.session.commit()

                # Delete event itself
                Event.query.filter_by(event_id=event.event_id).delete()

            db.session.commit()

        flash('All events deleted!', category='success')

        return redirect(url_for('base'))
    
    except Exception as e:
        db.session.rollback()

        print("Error deleting evetns: " + str(e))
        flash('Events not deleted, rolled back.', category='error')

        return redirect(url_for('base'))


@app.route('/add_one_club')
def add_one_club():
    try:
        # Isolates session
        with app.app_context():
            clubs = Club.query.all()
            
            for club in clubs:
                Event.query.filter_by(club_id=club.club_id).delete()
            
            
            Club.query.delete()

            club = Club(club_name="Pumpherston", club_url="https://www.pumpherstongolfclub.co.uk/", club_address="Drumshoreland Road, Pumpherston", club_postcode="EH53 0LQ", club_phone_number="01506 433337", approved=True)
            db.session.add(club)

            db.session.commit()
        
        flash('Club added!', category='success')

        return redirect(url_for('base'))
    
    except Exception as e:
        db.session.rollback()

        print("Error adding club: " + str(e))
        flash('Club not added, rolled back.', category='error')

        return redirect(url_for('base'))


@app.route('/add_multi_clubs')
def add_multi_clubs():
    try:
        # Isolates session
        with app.app_context():

            clubs = Club.query.all()
                
            for club in clubs:
                User_subscription.query.filter_by(club_id=club.club_id).delete()
                Event.query.filter_by(club_id=club.club_id).delete()
            
    

            club = Club(club_name="Pumpherston", club_url="https://www.pumpherstongolfclub.co.uk/", club_address="Drumshoreland Road, Pumpherston", club_postcode="EH53 0LQ", club_phone_number="01506 433337", approved=True)
            db.session.add(club)

            club = Club(club_name="Duddingston", club_url="https://www.duddingstongolfclub.co.uk/", club_address="Duddingston Golf Club, Duddingston Road West, Edinburgh", club_postcode="EH15 3QD", club_phone_number="0131 661 4301", approved=True)
            db.session.add(club)

            club = Club(club_name="Kings Acre", club_url="https://www.kings-acregolf.com/", club_address="Kings Acre Golf Club, Melville Mains, Lasswade", club_postcode="EH18 1AU", club_phone_number="0131 663 3456", approved=True)
            db.session.add(club)

            club = Club(club_name="Ratho Park", club_url="https://www.rathoparkgolfclub.co.uk/", club_address="Ratho Park Golf Club Ltd, Edinburgh", club_postcode="EH28 8NX", club_phone_number="0131 335 0068", approved=True)
            db.session.add(club)

            club = Club(club_name="Musselburgh", club_url="https://www.themusselburghgolfclub.com/", club_address="The Musselburgh Golf Club, Monktonhall, Musselburgh", club_postcode="EH21 6SA", club_phone_number="0131 665 7055", approved=True)
            db.session.add(club)

            club = Club(club_name="Dalmahoy", club_url="https://www.dalmahoyhotelandcountryclub.co.uk/golf-leisure/golf/golf-at-dalmahoy/", club_address="Dalmahoy Hotel & Country Club, Kirknewton, Edinburgh", club_postcode="EH27 8EB", club_phone_number="0131 333 1845", approved=True)
            db.session.add(club)

            club = Club(club_name="Murrayfield", club_url="https://www.murrayfieldgolfclub.co.uk/", club_address="Murrayfield Golf Club, 43 Murrayfield Road, Edinburgh", club_postcode="EH12 6EU", club_phone_number="0131 347 9961", approved=True)
            db.session.add(club)

            club = Club(club_name="Mortonhall", club_url="https://www.mortonhallgc.co.uk/", club_address="Mortonhall Golf Club, 231 Braid Road, Edinburgh", club_postcode="EH10 6PB", club_phone_number="0131 447 6974", approved=True)
            db.session.add(club)

            club = Club(club_name="Kingsknowe", club_url="https://www.kingsknowe.com/", club_address="Kingsknowe Golf Club, 326 Lanark Road, Edinburgh", club_postcode="EH14 2JD", club_phone_number="0131 441 4030", approved=True)
            db.session.add(club)

            club = Club(club_name="Craigmillar Park", club_url="https://www.craigmillarpark.co.uk/", club_address="Craigmillar Park Golf Club, 1 Observatory Road, Edinburgh", club_postcode="EH9 3HG", club_phone_number="0131 667 2837", approved=True)
            db.session.add(club)

            db.session.commit()

        flash('Multiple clubs added!', category='success')

        return redirect(url_for('base'))
    
    except Exception as e:
        db.session.rollback()

        print("Error adding multi clubs: " +  str(e))
        flash('Clubs not added, rolled back.', category='error')

        return redirect(url_for('base'))


# Deletes all clubs, this will also delete any associated subscriptions
# Note will not delete any associated events
@app.route('/delete_clubs')
def delete_clubs():
    try:
        # Isolates session
        with app.app_context():
            clubs = Club.query.all()
            
            for club in clubs:
                for subscription in club.subscriptions:
                    db.session.delete(subscription)
                db.session.delete(club)

            db.session.commit()

        flash('Clubs deleted!', category='success')

        return redirect(url_for('base'))
    
    except Exception as e:
        db.session.rollback()

        print("Error deleting clubs: " + str(e))
        flash('Clubs not deleted, rolled back.', category='error')

        return redirect(url_for('base'))



'''
------------------------------------------------------------------------------------------------------------------------------------------------
Other functions below here
    * validate_input
'''


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
    app.run(host='0.0.0.0', debug=True, port=8080)



