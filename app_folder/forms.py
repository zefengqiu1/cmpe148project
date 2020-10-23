from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectField,DateField,TimeField,HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app_folder.models import User
from datetime import time

class LoginForm(FlaskForm):
    username = StringField('Username',render_kw={"placeholder": "Username"})
    password = PasswordField('Password',render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign In')
    remember_me = BooleanField('Remember Me')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Invalid Username or Password')
        elif not user.check_password(self.password.data):
            raise ValidationError('Invalid Username or Password')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder": "123@gmail.com"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    password2 = PasswordField('Comfirmed Password', validators=[DataRequired(), EqualTo('password','unmatched')],render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
 
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ForgetPasswordForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()],render_kw={"placeholder": "123@gmail.com"})
    submit = SubmitField('Confirm')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('User not found')

class NewPasswordForm(FlaskForm):
    password = StringField('New Password',validators=[DataRequired()],render_kw={"placeholder": "Password"})
    password2 = PasswordField('Comfirmed Password', validators=[DataRequired(), EqualTo('password','unmatched')],render_kw={"placeholder": "Password"})
    submit = SubmitField('Confirm')

class AvailableForm(FlaskForm):
    start_time = TimeField("Start Time",validators=[DataRequired()],format='%H:%M')
    end_time = TimeField("End Time",validators=[DataRequired()],format='%H:%M')
    length = SelectField('Meeting Length(mins)', choices=[('15', "15"), ('30', "30"), ('60', "60")],validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_end_time(self, end_time):
        if end_time.data<=self.start_time.data:
            raise ValidationError('Invalid end time')
        
class EventForm(FlaskForm):
    availabletime = SelectField('Select Time slot',validators=[DataRequired()])
    name= StringField("Name:",validators=[DataRequired()],render_kw={"placeholder": "Name"})
    description = TextAreaField('Description:',validators=[DataRequired()],render_kw={"placeholder": "Enter Here"})
    submit = SubmitField("Submit")

class EmailConfimationForm(FlaskForm):
    confirm=BooleanField("test")

class monthswitchForm(FlaskForm):
    dec=SubmitField("<")
    inc=SubmitField(">")
    value=HiddenField('dec')