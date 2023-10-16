from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length



class SignUpForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
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

class creationForm(FlaskForm):
    """Recipe form"""
    name=StringField("Enter your recipe's name", validators=[DataRequired()])
    image=StringField("enter an image url to display your recipe",validators=[DataRequired()])
    description=StringField("enter a description of your recipe",validators=[DataRequired()])
    ingredients= StringField("ingredients", validators= [DataRequired()])
    # instructions= StringField("instructions")


class userEditForm(FlaskForm):
    username = StringField('new username', validators=[DataRequired()])
    email = StringField('new E-mail', validators=[DataRequired(), Email()])
    Current_password = PasswordField('Enter your Current Password', validators=[Length(min=6)])
    password = PasswordField('new Password', validators=[Length(min=6)])

