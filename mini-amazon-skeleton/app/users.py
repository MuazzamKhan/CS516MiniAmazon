from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from werkzeug.datastructures import MultiDict
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.purchase import Purchase
from .models.product import Product

import datetime

from flask import Blueprint
bp = Blueprint('users', __name__)


# This is to store user information 
curr_user = User(0, "", "", "", "")

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
    home_address = StringField('Home Address')
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
                         form.lastname.data,
                         form.home_address.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)



class UpdateProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()], default=curr_user.firstname) 
    lastname = StringField('Last Name', validators=[DataRequired()], default=curr_user.lastname)
    address = StringField('Home Address', validators=[DataRequired()], default=curr_user.address)
    email = StringField('Email', validators=[DataRequired(), Email()], default=curr_user.email)
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        if email.data != curr_user.email and User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')



@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    global curr_user
    if request.method == "GET":
        form = UpdateProfileForm(formdata=MultiDict({"firstname": curr_user.firstname, "lastname": curr_user.lastname, "email": curr_user.email, "address": curr_user.address}))
    elif request.method == "POST":
        form = UpdateProfileForm()
    if form.validate_on_submit():
        curr_user.set_profile(form.email.data, form.firstname.data, form.lastname.data, form.address.data)
        if User.update_profile(curr_user.id, form.email.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data):
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
    deposit = IntegerField('deposit', validators=[], default=0)
    withdraw = IntegerField('withdraw', validators=[], default=0)
    submit = SubmitField('adjust balance')



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




@bp.route('/purchase_history', methods=['GET', 'POST'])
def purchase_history():

    if current_user.is_authenticated:
        
        if request.method == "GET":
            # purchases = Purchase.get_all_by_uid_since(current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
            ancient = datetime.datetime(1980, 9, 14, 0, 0, 0)
            now = datetime.datetime.now()
            purchases = Purchase.get_all_by_uid_since(0, ancient, now)
            potential_sellers = list(set([ p.sname for p in purchases ]))
            potential_items = list(set([ p.product for p in purchases ]))
            
            since = ancient.strftime("%Y-%m-%d")
            today = now.strftime("%Y-%m-%d")

            
            return render_template('purchase_history.html', 
                                    title='Purchase History', 
                                    purchase=purchases,
                                    potential_sellers=potential_sellers, 
                                    potential_items=potential_items, 
                                    search_seller="",
                                    search_product="",
                                    since=since,
                                    to=today)

        elif request.method == "POST":
            form_data = request.form
            input_seller_fullname = form_data['seller']
            input_seller = input_seller_fullname.split() 
            input_product = form_data['item'].lower()
            input_start_date = form_data['start_date']
            input_end_date = form_data['end_date']
            
            date_start, date_end = generateDateRange(input_start_date, input_end_date)
            datetime_start, datetime_end = datetime.datetime(date_start[0], date_start[1], date_start[2], 0, 0, 0), datetime.datetime(date_end[0], date_end[1], date_end[2], 23, 59, 59)
            
            product = '%' if len(input_product) == 0 else '%' + input_product + '%'
        
            seller_firstname = '%'
            seller_lastname = '%' 
            
            if len(input_seller) >= 2:
                seller_firstname = '%' + input_seller[0].lower() + '%'
                seller_lastname = '%' + input_seller[1].lower() + '%'
            elif len(input_seller) == 1:
                seller_firstname = '%' + input_seller[0].lower() + '%'
            

            purchases = Purchase.get_all_by_uid_since(0, datetime_start, datetime_end, product, seller_firstname, seller_lastname)
            potential_sellers = list(set([ p.sname for p in purchases ]))
            potential_items = list(set([ p.product for p in purchases ]))
            

            return render_template('purchase_history.html', 
                                    title='Purchase History', 
                                    purchase=purchases, 
                                    potential_sellers=potential_sellers, 
                                    potential_items=potential_items,
                                    search_seller=input_seller_fullname,
                                    search_product=input_product,
                                    since=datetime_start.strftime("%Y-%m-%d"),
                                    to=datetime_end.strftime("%Y-%m-%d"))
    else:
        form = LoginForm()
        return render_template('login.html', title='Sign In', form=form)



@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))



def generateDateRange(date1, date2):

    date1_year, date1_month, date1_day = list(map(int, date1.split("-")))
    date2_year, date2_month, date2_day = list(map(int, date2.split("-")))
    
    if date1_year > date2_year:
        return [ date2_year, date2_month, date2_day ], [date1_year, date1_month, date1_day]
    elif date1_year < date2_year:
        return [date1_year, date1_month, date1_day], [ date2_year, date2_month, date2_day ]
    else:
        if date1_month > date2_month:
            return [ date2_year, date2_month, date2_day ], [date1_year, date1_month, date1_day]
        elif date2_month > date1_month:
            return [date1_year, date1_month, date1_day], [ date2_year, date2_month, date2_day ]
        else:
            if date1_day > date2_day:
                return [ date2_year, date2_month, date2_day ], [date1_year, date1_month, date1_day]
            elif date2_day > date1_day:
                return [date1_year, date1_month, date1_day], [ date2_year, date2_month, date2_day ]
            else: 
                date1, date2
