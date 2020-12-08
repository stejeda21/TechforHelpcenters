from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

def connect_db(app):
    """Connect with Flask App"""
    db.app = app
    db.init_app(app)

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User Model"""
    
    __tablename__ = 'users'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True
    )
    
    username = db.Column(
        db.Text, 
        nullable=False,
        unique=True
    )
    
    password = db.Column(
        db.Text, 
        nullable=False
    )
    
    help_center = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )
    
    

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    @classmethod
    def signup(cls, username, password, help_center):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            help_center=help_center
        )

        db.session.add(user)
        return user
    



class Refugee(db.Model):
    """Refugee Model"""
    
    __tablename__ = 'refugees'
    
    refugee_id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True
    )
    
    firstname = db.Column(
        db.Text, 
        nullable=False,
        unique=True
    )
    
    lastname = db.Column(
        db.Text, 
        nullable=False,
        unique=True
    )
    
    phonenumber = db.Column(
        db.Text, 
        nullable=False,
        unique=True
    )
    
    helpcenter = db.Column(
        db.Text, 
        nullable=False
    )
    
    check_in_status = db.Column(
        db.Text, 
        nullable=False
    )

    
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.firstname} {self.lastname}"
    

    @classmethod
    def register(cls, firstname, lastname, phonenumber, helpcenter, check_in_status):
        """Register Refugee"""

        refugee = Refugee(
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber,
            helpcenter=helpcenter,
            check_in_status=check_in_status,
        )

        db.session.add(refugee)
        
        return refugee
    