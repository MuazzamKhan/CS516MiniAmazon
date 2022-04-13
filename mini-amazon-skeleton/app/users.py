from flask import render_template, redirect, url_for, flash, request, current_app as app, g
from werkzeug.urls import url_parse
from werkzeug.datastructures import MultiDict
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange

from .models.user import User
from .models.seller import Seller
from .models.purchase import Purchase
from .models.product import Product
from .models.inventory import Inventory
from .models.review import Review

from .order import orderBuyer
from .email import send_email

import datetime
import itertools

from itsdangerous import URLSafeTimedSerializer

from flask import Blueprint

bp = Blueprint('users', __name__)

# This is to store user information 
curr_user = User(0, "", "", "", "", False)

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
        user = User.get_by_auth(form.email.data.lower(), form.password.data)
        curr_user = user
        
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        elif not user.email_confirm:
            flash('Please activate your account first. Check confirmation email in your mailbox')
            return render_template('login.html', title='Sign In', form=form, resend_confirmation=True, input_email=form.email.data.lower())
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, resend_confirmation=False, input_email="")


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
                token,
                salt=app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
                )
    except:
        return False
    return email


@bp.route('/confirm/<token>')
def confirm_email(token):

    try:
        email = confirm_token(token)
        User.confirm_email(email)
        flash('Your email is activated! You can log in now. ')
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    
    return redirect(url_for('users.login'))    




class ResendConfirmation(FlaskForm):
    registered_email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Resend')
    
    def validate_email(self, registered_email):
        if not User.email_exists(registered_email.data.lower()):
            flash('Email not found in our system! Please register first.')
            return False
        return True



@bp.route('/resend_confirmation', methods=['GET', 'POST'])
def resend_confirmation():
    
    if request.method == "GET":
        form = ResendConfirmation(formdata=MultiDict({"registered_email": request.args.get('input_email') }))
    else: 
        form = ResendConfirmation()

    if form.validate_on_submit() and form.validate_email(form.registered_email):
        token = generate_confirmation_token(form.registered_email.data)
        confirm_url = url_for('users.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(form.registered_email.data.lower(), subject, html)
        flash("Activation email is resent. Please activate before login.")
        
        return redirect(url_for('users.login'))

    return render_template('resend_confirmation.html', title='Resend confirmation Email', form=form, input_email=form.registered_email.data.lower())


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
        if User.email_exists(email.data.lower()):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        
        token = generate_confirmation_token(form.email.data.lower())
        confirm_url = url_for('users.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(form.email.data.lower(), subject, html)

        if User.register(form.email.data.lower(),
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.home_address.data):
            flash('Congratulations, you are now a registered user! Before login please confirm your email first in your mailbox.')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)



class UpdateProfileForm(FlaskForm):

    firstname = StringField('First Name', validators=[DataRequired()], default=curr_user.firstname) 
    lastname = StringField('Last Name', validators=[DataRequired()], default=curr_user.lastname)
    address = StringField('Home Address', validators=[DataRequired()], default=curr_user.address)
    email = StringField('Email', validators=[DataRequired(), Email()], default=curr_user.email.lower())
    receive_notification = BooleanField("I want to reveive email notification", default=False)
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        if email.data != curr_user.email and User.email_exists(email.data.lower()):
            raise ValidationError('Already a user with this email.')



@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    global curr_user
    if request.method == "GET":
        form = UpdateProfileForm(formdata=MultiDict({"firstname": curr_user.firstname, "lastname": curr_user.lastname, "email": curr_user.email.lower(), "address": curr_user.address, "receive_notification": Seller.get_if_receive_notification(curr_user.id) }))
    elif request.method == "POST":
        form = UpdateProfileForm()
    if form.validate_on_submit():
        curr_user.set_profile(form.email.data.lower(), form.firstname.data, form.lastname.data, form.address.data)
        if User.update_profile(curr_user.id, form.email.data.lower(),
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data):
            print(Seller.isSeller(curr_user.id), curr_user.id)
            if Seller.isSeller(curr_user.id):
                if Seller.update_receive_notification(curr_user.id, form.receive_notification.data):
                    flash('Your user profile has been updated!')
                    return render_template('profile.html', title='Profile', form=form, is_seller=Seller.isSeller(curr_user.id)), {"Refresh": "1; url="+str(url_for('index.index'))}
            else:
                flash('Your user profile has been updated!')
                return render_template('profile.html', title='Profile', form=form, is_seller=Seller.isSeller(curr_user.id)), {"Refresh": "1; url="+str(url_for('index.index'))}
    return render_template('profile.html', title='Profile', form=form, is_seller=Seller.isSeller(curr_user.id))



class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField('First Name', validators=[DataRequired()]) 
    new_password = PasswordField('Password', validators=[DataRequired()])
    new_password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')



@bp.route('/password', methods=['GET', 'POST'])
def password():
    global curr_user
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if User.check_password(curr_user.email.lower(), form.old_password.data):
            
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



class ReviewForm(FlaskForm):
    display_name = StringField('Enter a name to be displayed with the review:', validators = [DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min = 1, max = 5, message = 'Enter a integer between 1 and 5')], default = 5) 
    title = StringField('Title', validators=[DataRequired()], default = "Product Review")
    body = StringField('Enter your review:')
    submit = SubmitField('Publish review')

@bp.route('/write_review/<pid>', methods=['GET', 'POST'])
def write_review(pid):
    global curr_user
    form = ReviewForm()
    if form.validate_on_submit():
        if User.leave_review(form.display_name.data, curr_user.id, pid, form.rating.data, form.title.data, form.body.data):
            flash('Thanks for leaving a review!')
            return render_template('leave_review.html', title='Leave a Review', form=form), {"Refresh": "1; url="+str(url_for('product.product', pid = pid))}
    return render_template('leave_review.html', title='Leave a Review', form=form)


@bp.route('/product/<pid>/<uid>', methods=['GET'])
def upvote_review(pid, uid):
    global curr_user
    User.upvote_review(int(pid), int(uid), curr_user.id)
    product = Product.get(pid)
    if product == None:
        return "Error! No such product exists!"

    inventory = Inventory.get_with_pid(product.id)
    
    reviews = Review.get_reviews_with_pid(product.id)

    stock = "In Stock"
    min_price = 0

    if inventory is None:
        stock = "Out of Stock"
    else:
        for listing in inventory:
            if listing.price < min_price or min_price == 0:
                min_price = listing.price

    #return render_template("product.html", product=product, stock=stock, display_price=min_price, inventory=inventory, reviews = reviews)
    return (''), 204


@bp.route('/purchase_history', methods=['GET', 'POST'])
def purchase_history():

    """ purchase_history - Show personal purchase history 

    Returns
    -------
    Flask page html
    """

    if current_user.is_authenticated:
        
        if request.method == "GET":
            ancient = datetime.datetime(1980, 9, 14, 0, 0, 0)
            now = datetime.datetime.now()
            purchases = Purchase.get_all_by_uid_since(curr_user.id, ancient, now)
                
            potential_sellers = []
            for p in purchases:
                for s in p.sname:
                    if s not in potential_sellers:
                        potential_sellers.append(s)
            
            potential_quantity = list(set([ p.quantity for p in purchases ]))
            
            since = ancient.strftime("%Y-%m-%d")
            today = now.strftime("%Y-%m-%d")

            return render_template('purchase_history.html', 
                                    title='Purchase History', 
                                    purchase=purchases,
                                    potential_sellers=potential_sellers, 
                                    potential_quantity=potential_quantity, 
                                    search_seller="",
                                    search_quantity="",
                                    since=since,
                                    to=today)

        elif request.method == "POST":
            form_data = request.form
            input_seller_fullname = form_data['seller']
            input_seller = input_seller_fullname.split() 
            input_quantity = form_data['item']
            input_start_date = form_data['start_date']
            input_end_date = form_data['end_date']
            
            # pass user inputs as filter to the query
            date_start, date_end = generateDateRange(input_start_date, input_end_date)
            datetime_start, datetime_end = datetime.datetime(date_start[0], date_start[1], date_start[2], 0, 0, 0), datetime.datetime(date_end[0], date_end[1], date_end[2], 23, 59, 59)
            
            quantity = int(input_quantity) if input_quantity.isnumeric() else -1
        
            seller_firstname = '%'
            seller_lastname = '%' 
            
            if len(input_seller) >= 2:
                seller_firstname = '%' + input_seller[0].lower() + '%'
                # seller_firstname = input_seller[0].lower() 
                seller_lastname = '%' + input_seller[1].lower() + '%'
                # seller_lastname = input_seller[1].lower()
            elif len(input_seller) == 1:
                seller_firstname = '%' + input_seller[0].lower() + '%'
                # seller_firstname = input_seller[0].lower() 
            

            purchases = Purchase.get_all_by_uid_since(curr_user.id, datetime_start, datetime_end, quantity, seller_firstname, seller_lastname)
            
            potential_sellers = []
            for p in purchases:
                for s in p.sname:
                    if s not in potential_sellers:
                        potential_sellers.append(s)
            

            potential_quantity = list(set([ p.quantity for p in purchases ]))
            
            if quantity == -1: quantity = ""

            return render_template('purchase_history.html', 
                                    title='Purchase History', 
                                    purchase=purchases, 
                                    potential_sellers=potential_sellers, 
                                    potential_quantity=potential_quantity,
                                    search_seller=input_seller_fullname,
                                    search_quantity=quantity,
                                    since=datetime_start.strftime("%Y-%m-%d"),
                                    to=datetime_end.strftime("%Y-%m-%d"))
    else:
        form = LoginForm()
        return render_template('login.html', title='Sign In', form=form, resend_confirmation=False, input_email="")



@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))



@bp.route('/user_public_view/<int:id>')
def user_public_view(id):
    """user_public_view - Show public view page for a given user

    Parameters
    ----------
    id : int
        User id

    Returns
    -------
    Public view html        
    """
    user = User.get(id)

    return render_template('user_public_view.html', title='Public view', user=user)

@bp.route('/submitted-reviews/<id>')
def submitted_reviews(id):
    reviews = Review.get_reviews_with_uid(id)
    return render_template('reviews.html', reviews=reviews, id=id)



def generateDateRange(date1, date2):
    """generateDateRange - Generate a date range regardless the order of two given dates

    Parameters
    ----------
    date1 : String
        Date 1 (i.e. "2020-12-12")
    date2 : String
        Date 2 

    Returns
    -------
    List, List
        Each list is [ year, month, date ], the first list is before the second list
    """

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
                return [date1_year, date1_month, date1_day], [ date2_year, date2_month, date2_day ]
