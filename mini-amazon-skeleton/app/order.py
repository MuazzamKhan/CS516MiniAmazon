from flask import render_template, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, NumberRange, Length
from flask_babel import _, lazy_gettext as _l

from .models.order import Order
from .models.user import User

from flask import Blueprint
bp = Blueprint('order', __name__)

@bp.route('/order/<uid>', methods=['GET'])
def order(uid):
    orders = Order.get_by_uid(uid)
    if orders == None:
        flash("This user has not made any order!")
        return
    else:
        return render_template("order.html", orders=orders)