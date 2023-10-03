from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length



class SignUpForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    country=StringField("what country are you from?",validators=[Length(min=6)])
    password = PasswordField('create your password', validators=[Length(min=6)])

class EditPassword(FlaskForm):
     """Form for editing users."""
     Current_password = PasswordField('Current Password', validators=[Length(min=6)])
     new_password=PasswordField('New Password', validators=[Length(min=6)])
     confirm_password=PasswordField('confirm your password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])