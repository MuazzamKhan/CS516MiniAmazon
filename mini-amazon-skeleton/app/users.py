from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from werkzeug.datastructures import MultiDict
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)


# This is to store user information 
curr_user = User(0, "", "", "")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')





@bp.route('/login', methods=['GET', 'POST'])
def login():
    
    global curr_user

    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        curr_user = user
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)



class UpdateProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()], default=curr_user.firstname) 
    lastname = StringField('Last Name', validators=[DataRequired()], default=curr_user.lastname)
    email = StringField('Email', validators=[DataRequired(), Email()], default=curr_user.email)
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        if email.data != curr_user.email and User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')



@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    global curr_user
    if request.method == "GET":
        form = UpdateProfileForm(formdata=MultiDict({"firstname": curr_user.firstname, "lastname": curr_user.lastname, "email": curr_user.email}))
    elif request.method == "POST":
        form = UpdateProfileForm()
    if form.validate_on_submit():
        curr_user.set_profile(form.email.data, form.firstname.data, form.lastname.data)
        if User.update_profile(curr_user.id, form.email.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Your user profile has been updated!')
            return render_template('profile.html', title='Profile', form=form), {"Refresh": "1; url="+str(url_for('index.index'))}
    return render_template('profile.html', title='Profile', form=form)



class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField('First Name', validators=[DataRequired()]) 
    new_password = PasswordField('Password', validators=[DataRequired()])
    new_password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Profile')



@bp.route('/password', methods=['GET', 'POST'])
def password():
    global curr_user
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if User.check_password(curr_user.email, form.old_password.data):
            
            User.update_password(curr_user.id, form.new_password.data)
            flash('Your password has been changed successfully!')
            
            return render_template('password.html', title='Password', form=form), {"Refresh": "1; url="+str(url_for('index.index'))}
        else:
            flash('Old password is incorrect.')
    return render_template('password.html', title='Password', form=form)



class BalanceForm(FlaskForm):
    deposit = IntegerField('Deposit', validators=[], default=0)
    withdraw = IntegerField('Withdraw', validators=[], default=0)
    submit = SubmitField('Adjust Balance')



@bp.route('/balance', methods=['GET', 'POST'])
def balance():
    form = BalanceForm()
    if form.validate_on_submit():
        if User.update_balance(curr_user.id, form.deposit.data, form.withdraw.data):
            flash('Your balance has been updated successfully!')
            return render_template('balance.html', title='Balance', form=form, current_balance=User.get_balance(curr_user.id)), {"Refresh": "1; url="+str(url_for('index.index'))}
        else:
            flash('You do not have enough money to withdraw!')            
    return render_template('balance.html', title='Balance', form=form, current_balance=User.get_balance(curr_user.id))



@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
