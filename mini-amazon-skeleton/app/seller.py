from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, SelectField
from wtforms.validators import ValidationError, InputRequired, NumberRange, Required, Length
from flask_wtf.file import FileField, FileRequired

from .models.seller import Seller

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
        return render_template("seller_page.html", sid=sid)
