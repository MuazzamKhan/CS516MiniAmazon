from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, NumberRange, Required
from werkzeug.utils import secure_filename

from .models.inventoryitem import InventoryItem
from .models.user import User
from .models.product import Product
from .models.categories import categories
import os
import app

from flask import Blueprint
bp = Blueprint('inventory', __name__)

@bp.route('/inventory/<seller_id>', methods=['GET'])
def inventory(seller_id):
    user = User.get(seller_id)

    if user.is_seller is False:
        flash("This user is not a seller! No inventory can be displayed.")
        return redirect(url_for('index.index', page_number = 1))

    inventory = Inventory.get_by_seller(seller_id)
    return render_template("inventory.html", inventory_items = inventory)\

class NewInventoryForm(FlaskForm):
    product_id = IntegerField(_l('Product ID'), validators=[InputRequired()])
    name = StringField(_l('Product Name'), validators=[InputRequired()])
    description = TextField(_l('Description'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[InputRequired(), NumberRange(min=0, message="Price must be >= $0")])
    quantity = IntegerField(_l('Quantity'), validators=[InputRequired(), NumberRange(min=0, message="Quantity must be >= 0 units")])
    submit = SubmitField(_l('Add Inventory'))

# add an item to inventory/product db
@bp.route('/addinventory', methods=['GET', 'POST'])
def addInventory():
    form = NewInventoryForm()
    seller_id = current_user.id
    if form.validate_on_submit():
        new_item = Inventory.add_item(product_id, seller_id, price, quantity)
        flash('Successfully added to inventory!')
        inventory = Inventory.get_by_seller(seller_id)
        return redirect(url_for("inventory.inventory", seller_id = seller_id))
    return render_template('addinventory.html', title = 'Add to Inventory', form = form)