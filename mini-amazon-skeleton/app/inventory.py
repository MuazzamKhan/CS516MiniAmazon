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
        return "This user is not a seller. No inventory can be shown!"
    else:
        return render_template("inventory.html", inventory=inventory)

class EditInventoryForm(FlaskForm):
    price = DecimalField('Enter New Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be >= $0")])
    quantity = IntegerField('Enter New Quantity', validators=[InputRequired(), NumberRange(min=0, message="Quanitity must be >= 1 units")])
    submit = SubmitField('Confirm Change to Inventory')

@bp.route('/edit-inventory/<pid>/<sid>', methods=['GET', 'POST'])
def editInventory(pid, sid):
    print(pid)
    inventory = Inventory.get_with_pid(pid)
    form = EditInventoryForm()
    if request.method=='POST':
        price = float(request.form.get("price"))
        if price < 0:
            flash("Invalid price input")
            return redirect(url_for('inventory.inventory'))
        quantity = int(request.form.get("quantity"))
        if quantity < 0:
            flash("Invalid quantity input")
            return redirect(url_for('inventory.inventory'))
    if form.validate_on_submit():
        print("check 2")
        Inventory.edit_price(pid, sid, form.price.data)
        Inventory.edit_quantity(pid, sid, form.quantity.data)
        flash("Successfully changed price for product")
        return redirect(url_for('inventory.inventory', sid=0))
    return render_template('edit_product.html', form=form, inventory=inventory, pid=1, sid=0)


class NewInventoryForm(FlaskForm):
    pid = IntegerField('Product ID', validators=[InputRequired()])
    name = StringField('Product Name', validators=[InputRequired()])
    description = TextField('Description', validators=[InputRequired(), Length(max=200)])
    price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be >= $0")])
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=0, message="Quantity must be >= 0 units")])
    submit = SubmitField('Add Inventory')


@bp.route('/add-inventory/<sid>', methods=['GET','POST'])
def addInventory(sid):
    form = NewInventoryForm()
    if form.validate_on_submit():
        new_item = Inventory.add_item(form.pid.data, sid, form.price.data, form.quantity.data)
        flash('Successfully added new item to inventory!')
        return redirect(url_for("inventory.inventory", sid=current_user.id))
    return render_template('add_inventory.html', title='Add to Inventory', form=form, sid=sid)

class RemoveInventoryForm(FlaskForm):
    pid = IntegerField('Product ID', validators=[InputRequired()])
    submit = SubmitField('Remove Inventory')

@bp.route('/remove-inventory/<pid>', methods=['GET','POST'])
def removeInventory(pid):
    form = RemoveInventoryForm()
    if form.validate_on_submit():
        Inventory.remove_item(sid, pid)
        flash('Successfully removed item from inventory!')
        return redirect(url_for("inventory.inventory", sid=current_user.id))
    return render_template('remove_inventory.html', title='Remove from Inventory', form=form, inventory=inventory, pid=pid)


