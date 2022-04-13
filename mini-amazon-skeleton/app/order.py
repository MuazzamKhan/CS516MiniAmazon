from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired, NumberRange, Length
from flask_babel import _, lazy_gettext as _l

from .models.order import Order, OrderSummary
from .models.user import User

from flask import Blueprint
bp = Blueprint('order', __name__)

@bp.route('/buyer-order/<bid>/<oid>', methods=['GET'])
def orderBuyer(bid, oid):
    orders = Order.get_by_bid_oid(bid, oid)
    #print(bid)
    return render_template("order.html", orders=orders, bid=bid, oid=oid)


@bp.route('/seller-order/<sid>', methods=['GET'])
def orderSeller(sid):
    orders = OrderSummary.get_by_sid(sid)
    return render_template("order_seller.html", orders=orders, sid=sid)

@bp.route('/seller-order-details/<sid>/<oid>', methods=['GET'])
def orderSellerDetails(sid, oid):
    orders = Order.get_by_sid_oid(sid, oid)
    return render_template("order_seller_detailed.html", orders=orders, sid=sid, oid=oid)


class ItemFulfilledForm(FlaskForm):
    confirm = SelectField('Confirm that this product is fulfilled? (Y/N)', choices=["Yes", "No"])
    submit = SubmitField('Submit')


@bp.route('/seller-order/item-fulfilled/<sid>/<oid>/<pid>', methods=['GET','POST'])
def itemFulfilled(oid, sid, pid):
    form = ItemFulfilledForm()
    confirmation = form.confirm.data
    #print("confirmation", confirmation)
    if confirmation == "No":
        flash('You indicated that this item is NOT fulfilled.')
        return redirect(url_for("order.itemFulfilled", sid = sid, oid=oid, pid=pid))
    if confirmation == "Yes":
        if form.validate_on_submit():
            Order.item_fulfilled(oid, pid)
            Order.all_fulfilled_check(oid)
            flash('You indicated that this item is SUCCESSFULLY fulfilled.')
            return redirect(url_for("order.itemFulfilled", sid = sid, oid=oid, pid=pid))
    return render_template('item_fulfilled.html', title='Item Fulfilled', form=form, sid=sid, oid=oid, pid=pid)

class SearchForm(FlaskForm):
    oid = StringField('Order ID (Enter \'NA\' if field not needed)')
    address = StringField('Address (Enter \'NA\' if field not needed)')
    time_placed_start = DateTimeLocalField('Time Placed - From', format="%Y-%m-%dT%H:%M")
    time_placed_end = DateTimeLocalField('Time Placed - To', format="%Y-%m-%dT%H:%M")
    submit = SubmitField('Submit')

@bp.route('/seller-order/search/<sid>', methods=['GET', 'Post'])
def orderSearch(sid):
    form = SearchForm()
    if form.validate_on_submit():
        orders = OrderSummary.get_by_search(sid, form.time_placed_start.data, form.time_placed_end.data, form.oid.data, form.address.data)
        if orders == None:
            return "Error! No orders for your search criteria exists!"
        if orders == "oid input error":
            return "Error in Order ID input!"
        return render_template("order_seller.html", orders=orders, sid=sid)
    return render_template("order_search.html", title='Search Options', form=form, sid=sid)

""" class SearchForm(FlaskForm):
    product_name = StringField('Product Name (Enter \'NA\' if field not needed)')
    pid = StringField('Product ID (Enter \'NA\' if field not needed)')
    oid = StringField('Order ID (Enter \'NA\' if field not needed)')
    address = StringField('Address (Enter \'NA\' if field not needed)')
    time_placed_start = DateTimeLocalField('Time Placed - From', format="%Y-%m-%dT%H:%M")
    time_placed_end = DateTimeLocalField('Time Placed - To', format="%Y-%m-%dT%H:%M")
    submit = SubmitField('Submit')

@bp.route('/seller-order/search/<sid>', methods=['GET', 'Post'])
def orderSearch(sid):
    form = SearchForm()
    if form.validate_on_submit():
        orders = Order.get_by_search(sid, form.time_placed_start.data, form.time_placed_end.data, form.product_name.data, form.pid.data, form.oid.data, form.address.data)
        if orders == None:
            return "Error! No orders for your search criteria exists!"
        if orders == "pid input error":
            return "Error in Product ID input!"
        if orders == "oid input error":
            return "Error in Order ID input!"
        return render_template("order_seller.html", orders=orders, sid=sid)
    return render_template("order_search.html", title='Search Options', form=form, sid=sid)
 """