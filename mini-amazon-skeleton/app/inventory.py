from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, SelectField
from wtforms.validators import ValidationError, InputRequired, NumberRange, Required, Length

from .models.inventory import Inventory
from .models.user import User
from .models.product import Product

import os
import app

from flask import Blueprint
bp = Blueprint('inventory', __name__)

@bp.route('/inventory/<sid>', methods=['GET'])
def inventory(sid):
    inventory = Inventory.get_with_sid(sid)
    if inventory == None:
        flash("This user is not a seller. No inventory can be shown!")
        return
    else:
        return render_template("inventory.html", inventory=inventory)


class NewInventoryForm(FlaskForm):
    pid = IntegerField('Product ID', validators=[InputRequired()])
    name = StringField('Product Name', validators=[InputRequired()])
    description = TextField('Description', validators=[InputRequired(), Length(max=200)])
    price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be >= $0")])
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=0, message="Quantity must be >= 0 units")])
    submit = SubmitField('Add Inventory')


@bp.route('/add-inventory', methods=['GET', 'POST'])
def addInventory():
    form = NewInventoryForm()
    if form.validate_on_submit():
        new_item = Inventory.add_item(pid, sid, price, quantity)
        flash('Successfully added new item to inventory!')
        inventory = Inventory.get_by_seller(sid)
        return redirect(url_for("inventory.inventory", sid=sid))
    return render_template('add_inventory.html', title='Add to Inventory', form=form)

class RemoveInventoryForm(FlaskForm):
    pid = IntegerField('Product ID', validators=[InputRequired()])
    submit = SubmitField('Remove Inventory')

@bp.route('/remove-inventory')
def removeInventory():
    form = RemoveInventoryForm()
    if form.validate_on_submit():
        Inventory.remove_item(sid, pid)
        flash('Successfully removed item from inventory!')
        return redirect(url_for("inventory.inventory", sid = sid))
    return render_template('remove_inventory.html', title='Remove from Inventory', form=form)


class EditQuantityForm(FlaskForm):
    quantity = IntegerField('Enter New Quantity', validators=[InputRequired(), NumberRange(min=0, message="Quanitity must be >= 0 units")])
    submit = SubmitField('Confirm Quantity Change')

# page for editing quantity of inventory
@bp.route('/edit-quantity/<int:pid>', methods=['GET', 'POST'])
def editQuantity(pid):
    form = EditQuantityForm()
    price = request.form['quantity']
    if quantity < 0:
        flash("Invalid quantity input")
        return redirect(url_for('inventory.inventory'))
    if form.validate_on_submit():
        Inventory.edit_quantity(pid, sid, form.quantity.data)
        flash("Successfully changed price for product")
        return redirect(url_for('inventory.inventory'))
    return render_template('edit_quantity.html',form=form)

class EditPriceForm(FlaskForm):
    price = DecimalField('Enter New Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be >= $0")])
    submit = SubmitField('Confirm Price Change')

# page for editing price of inventory
@bp.route('/edit-price/<int:pid>', methods=['GET', 'POST'])
def editPrice(pid):
    form = EditPriceForm()
    price = request.form['price']
    if price < 0:
        flash("Invalid price input")
        return redirect(url_for('inventory.inventory'))
    if form.validate_on_submit():
        Inventory.edit_price(pid, sid, form.price.data)
        flash("Successfully changed price for product")
        return redirect(url_for('inventory.inventory'))
    return render_template('editprice.html', form=form)

