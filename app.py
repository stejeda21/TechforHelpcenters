"""Import methods"""
import os
from flask import Flask, render_template, request, session, g, redirect, flash
from models import db, connect_db, User, Refugee
from twilio.rest import Client
from sqlalchemy import exc
import requests
from twilio.request_validator import RequestValidator
from sqlalchemy.sql import text

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///test_db'))
app.config['SECRET_KEY'] = os.environ.get('fdjako;fjo', "fdjskao;o;sda")

connect_db(app)

CURRENT_USER_KEY = "current_user"

"""Methods for logging in and logging out."""

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURRENT_USER_KEY in session:
        g.user = User.query.get(session[CURRENT_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session[CURRENT_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURRENT_USER_KEY in session:
        del session[CURRENT_USER_KEY]


##################################################################################################

"""User Registration"""

@app.route('/user-registration', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    - Create new user and add to DB. Redirect to home page.
    - If form not valid, present form.
    - If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURRENT_USER_KEY in session:
        del session[CURRENT_USER_KEY]
        
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        help_center = request.form['help_center']
         
        try:
            user = User.signup(
                username=username,
                password=password,
                help_center=help_center
            )
            db.session.commit()
        
        except exc.IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('user-registration.html')
        
        do_login(user)
        return redirect("/refugees")

    else: 
        return render_template('user-registration.html')
###################################################################################################
    
@app.route("/")
def home():
    """Render Home page"""
    return render_template('home.html')
###################################################################################################
"""User login"""

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    
    
    if request.method == "POST":
        user = User.authenticate(request.form['username'],
                                 request.form['password'])
        
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!")
            return redirect("/refugees")
        
        flash("Invalid credentials.", 'danger')
    users = User.query.all()
    return render_template('login.html', users=users)

###################################################################################################
@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

###################################################################################################
@app.route('/refugees', methods=["GET", "POST"])
def show():
    """Show all Refugees"""
    
    g.user = User.query.get(session[CURRENT_USER_KEY])
    refugees = Refugee.query.filter(Refugee.helpcenter == g.user.help_center)
    # refugees = Refugee.query.all()
    return render_template('show.html', refugees=refugees)
###################################################################################################
@app.route('/refugees/all', methods=["GET", "POST"])
def all():
    """Show all Refugees"""
    
    refugees = Refugee.query.all()
    return render_template('show.html', refugees=refugees)
  
###################################################################################################
@app.route('/refugees/status')
def status():
    number_of_refugees_checked_in = Refugee.query.all();
###################################################################################################
@app.route('/refugees/<int:refugee_id>')
def refugees_show(refugee_id):
    """Show a page with info on a specific refugee"""

    refugees = Refugee.query.get_or_404(refugee_id)
    return render_template('show.html', refugees=refugees)
###################################################################################################
@app.route('/refugees/<int:refugee_id>/edit')
def refugees_edit(refugee_id):
    """Show a page with info on a specific refugee"""

    refugee = Refugee.query.get_or_404(refugee_id)
    return render_template('edit.html', refugee=refugee)

###################################################################################################
@app.route('/refugees/<int:refugee_id>/delete', methods=["POST"])
def refugee_delete(refugee_id):
    """Handle form submission for deleting an existing user"""

    refugee = Refugee.query.get_or_404(refugee_id)
    db.session.delete(refugee)
    db.session.commit()
    flash(f"Refugee {refugee.full_name} was successfully deleted.")

    return redirect("/refugees")
###################################################################################################

@app.route('/refugees/<int:refugee_id>/edit', methods=["POST"]) #Dont forget to add POST Method
def update_refugee(refugee_id):
    """Handle form submission for updating an existing refugee"""

    refugee = Refugee.query.get_or_404(refugee_id)
    refugee.firstname = request.form['firstname']
    refugee.lastname = request.form['lastname']
    refugee.phonenumber = request.form['phonenumber']
    refugee.check_in_status = request.form['status']
    refugee.helpcenter = request.form['helpcenter']

    db.session.add(refugee)
    db.session.commit()
    flash(f"Refugee {refugee.full_name} edited.")

    return redirect("/refugees")
###################################################################################################
"""TWILIO API REQUEST TO SEND SMS"""
@app.route('/refugees/<int:refugee_id>/edit/SMS', methods=["POST"])
def send_sms(refugee_id):
    ACCOUNTSID = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE']
    MY_PHONE_NUMBER = os.environ['MY_PHONE_NUMBER']
    API_BASE_URL ='https://api.twilio.com/2010-04-01'
    
    refugee = Refugee.query.get_or_404(refugee_id)
    refugee.firstname = request.form['firstname']
    refugee.lastname = request.form['lastname']
    refugee.phonenumber = request.form['phonenumber']
    refugee.check_in_status = request.form['status']
    refugee.helpcenter = request.form['helpcenter']

    db.session.add(refugee)
    db.session.commit()
    flash(f"{refugee.full_name}'s status is updated. SMS notification sent!")


    url = f'{API_BASE_URL}/Accounts/{ACCOUNTSID}/Messages?To={refugee.phonenumber}&From={TWILIO_PHONE_NUMBER}&Body=Thank you, {refugee.firstname}! You have succesfully {refugee.check_in_status} from {refugee.helpcenter}!'

    payload=f'To=%2B19083728419*&From=%2B19084023124&Body=Thank%20you%2C%20%7B{refugee.full_name}%7D!%20You%20have%20succesfully%20%7B{refugee.check_in_status}%7D%20from%20%7B{refugee.helpcenter}%7D!'
    headers = {
    'Authorization': 'Basic QUNkMDFmNmRkYWI2MjRlMDM2N2EzYzZjMGMwMDAzODU3YzozYmIyZmY5MzI4ZThiYWI0N2VmNmI3OGQwZjdjNDAxYg==',
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return redirect("/refugees")
###################################################################################################
@app.route("/refugees/capacity", methods=["POST", "GET"])
def capacity_update():
    ACCOUNTSID = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE']
    MY_PHONE_NUMBER = os.environ['MY_PHONE_NUMBER']
    API_BASE_URL ='https://api.twilio.com/2010-04-01'

    refugees = Refugee.query.all()
    for refugee in refugees:
        firstname = refugee.firstname
        user = User.query.get(session[CURRENT_USER_KEY])

        url = f'{API_BASE_URL}?To=+19083728419&From=+19084023124&Body=Hi {firstname}, unfortunately {user.help_center}s capacity is full. The other help centers that have open occupancy are: {refugee.helpcenter}'
        payload='To=%2B19083728419&From=%2B19084023124&Body=Hi%20%7BRefugee.firstname%7D%2C%20unfortunately%20%7Buser.help_center%7Ds%20capacity%20is%20full.%20The%20other%20help%20centers%20that%20have%20open%20occupancy%20are%3A%20%7Bopen_helpcenters%7D'
        headers = {'Authorization': 'Basic QUNkMDFmNmRkYWI2MjRlMDM2N2EzYzZjMGMwMDAzODU3YzozYmIyZmY5MzI4ZThiYWI0N2VmNmI3OGQwZjdjNDAxYg==','Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, headers=headers, data=payload)

    flash(f"Capacity update notification has been successfully sent to Refugees!")
    return redirect("/refugees")

###################################################################################################
"""Refugee Registration"""

@app.route('/refugee-registration', methods=["GET", "POST"])
def register():
    """Render Refugee Registration"""
    
    if request.method == "POST":
        try:
           
            refugee = Refugee.register(
                firstname = request.form['firstname'],
                lastname = request.form['lastname'],
                phonenumber = request.form['phonenumber'],
                helpcenter = request.form['helpcenter'],
                check_in_status = request.form['status'],
                
            )
            
            db.session.commit()

        except exc.IntegrityError:
            flash('Invalid information')
            return render_template('registration.html')

        return redirect("/refugees")

    else:
        
        return render_template('registration.html')
###################################################################################################




