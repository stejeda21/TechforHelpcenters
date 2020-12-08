from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Length, DataRequired

class UserRegistration(FlaskForm):
    """Form for user registration"""

username = StringField('Create username', validators=[DataRequired()])
password = PasswordField('Create password', validators=[Length(min=6)])
help_center = SelectField('help_center', choices=[('SA', 'Salvation Army'), ('TH', 'Traditional Housing'), ('YCS', 'YMCA County Shelter'), ('VH', 'Village for Humanity')])
   
class RefugeeRegistration(FlaskForm):
   """Form for refugee registration"""
   
first_name = StringField('First name', validators=[DataRequired()])
last_name  = StringField('Last name', validators=[DataRequired()])
help_center = SelectField('help_center', choices=[('SA', 'Salvation Army'), ('TH', 'Traditional Housing'), ('YCS', 'YMCA County Shelter'), ('VH', 'Village for Humanity')])