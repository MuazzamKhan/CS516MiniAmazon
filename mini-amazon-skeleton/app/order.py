from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, SelectField
from wtforms.validators import InputRequired, NumberRange, Length
from flask_babel import _, lazy_gettext as _l

from .models.order import Order
from .models.user import User

from flask import Blueprint
bp = Blueprint('order', __name__)

@bp.route('/buyer-order/<uid>', methods=['GET'])
def orderBuyer(uid):
    orders = Order.get_by_uid(uid)
    if orders == None:
        return "Error! No such buyer exists!"
    else:
        return render_template("order.html", orders=orders)


@bp.route('/seller-order/<sid>', methods=['GET'])
def orderSeller(sid):
    orders = Order.get_by_sid(sid)
    if orders == None:
        return "Error! No such seller exists!"
    else:
        return render_template("order_seller.html", orders=orders)


class MarkFufilledForm(FlaskForm):
    confirm = StringField('Confirm fulfilment? (Yes/No)')
    submit = SubmitField('Submit')


@bp.route('/seller/mark-fulfill', methods=['GET'])
def markFulfilled():
    form = MarkFufilledForm()
    confirmation = request.form.get("confirm")
    if confirmation == 'No':
        flash('You indicated that this order is NOT fulfilled.')
        return redirect(url_for("order.orderSeller", sid=sid))
    if form.validate_on_submit():
        Order.mark_fulfilled(id, pid)
        flash('You indicated that this order is SUCCESSFULLY fulfilled.')
        return redirect(url_for("order.orderSeller", sid = sid))
    return render_template('mark_fulfilled.html', title='Mark Fulfilled', form=form)