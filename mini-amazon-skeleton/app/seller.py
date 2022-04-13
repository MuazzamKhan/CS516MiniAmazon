from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, SelectField
from wtforms.validators import ValidationError, InputRequired, NumberRange, Required, Length
from flask_wtf.file import FileField, FileRequired

from .models.seller import Seller
from .models.review import Review


import os
import app

from flask import Blueprint
bp = Blueprint('seller', __name__)

@bp.route('/seller-page/<sid>', methods=['GET'])
def seller(sid):
    isSeller = Seller.isSeller(sid)
    if isSeller == False:
        return "This user is not a seller. No seller's page can be shown!"
    else:
        reviews = Review.get_reviews_with_uid(sid)
        return render_template("seller_page.html", sid=sid, reviews=reviews)

class beSellerForm(FlaskForm):
    confirm = SelectField('Do you want to be a seller? (Y/N)', choices=["Yes", "No"])
    submit = SubmitField('Submit')

@bp.route('/be-seller/<uid>', methods=['GET', 'POST'])
def beSeller(uid):
    form = beSellerForm()
    confirmation = form.confirm.data
    if form.validate_on_submit():
        if confirmation == "No":
            return redirect(url_for("seller.beSeller", uid=uid))
        else:
            beSeller = Seller.beSeller(uid)
            if beSeller == False:
                flash("You are already a seller!")
                return redirect(url_for("seller.beSeller", uid=uid))
            flash("You are now a seller!")
            return redirect(url_for("seller.beSeller", uid=uid))
    return render_template("be_seller.html", form=form, uid=uid)


