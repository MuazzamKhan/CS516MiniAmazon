from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, SelectField
from wtforms.validators import ValidationError, InputRequired, NumberRange, Required, Length
from flask_wtf.file import FileField, FileRequired

from .models.inventory import Inventory
from .models.user import User
from .models.product import Product
from .models.seller import Seller
from .models.seller_analytics import Product_Rank, Category_Rank, Inventory_Analytics, Seller_Review_Analytics, Product_Review_Analytics


import os
import app

from flask import Blueprint
bp = Blueprint('inventory', __name__)

categories = [('Books', 'Books'), ('Clothing', 'Clothing'), ('Electronics', 'Electronics'), ('Food', 'Food'), ('Home', 'Home'), ('Media', 'Media'), ('Toys', 'Toys'), ('Sports', 'Sports')]

@bp.route('/inventory/<sid>', methods=['GET'])
def inventory(sid):
    inventory = Inventory.get_with_sid(sid)
    unique_inventory = Inventory_Analytics.calc_unique_items(sid)
    total_inventory = Inventory_Analytics.calc_total_quantity(sid)
    avg_price_inventory = Inventory_Analytics.calc_average_price(sid)
    return render_template("inventory.html", 
    inventory=inventory,
    total_inventory=total_inventory, 
    unique_inventory=unique_inventory, 
    avg_price_inventory=avg_price_inventory)

class EditInventoryForm(FlaskForm):
    price = DecimalField('Enter New Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be >= $0")])
    quantity = IntegerField('Enter New Quantity', validators=[InputRequired(), NumberRange(min=0, message="Quanitity must be >= 1 units")])
    submit = SubmitField('Confirm Change to Inventory')

@bp.route('/edit-inventory/<pid>/<sid>', methods=['GET', 'POST'])
def editInventory(pid, sid):
    #print(pid)
    inventory = Inventory.get_with_pid(pid)
    form = EditInventoryForm()
    if form.validate_on_submit():
        #print("check 2")
        Inventory.edit_price(pid, sid, form.price.data)
        Inventory.edit_quantity(pid, sid, form.quantity.data)
        flash("Successfully changed price for product")
        return redirect(url_for('inventory.inventory', sid=sid))
    return render_template('edit_product.html', form=form, inventory=inventory, pid=pid, sid=sid)


class AddUnlistedProductForm(FlaskForm):
    name = StringField('Product Name', validators=[InputRequired()])
    description = TextField('Description', validators=[InputRequired(), Length(max=200)])
    price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be >= $0")])
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=0, message="Quantity must be >= 0 units")])
    category = SelectField('Category', choices=categories)
    image_file = FileField('Product Image', validators=[FileRequired()])
    submit = SubmitField('Add Product')


@bp.route('/add-unlisted-Product/<sid>', methods=['GET','POST'])
def addUnlistedProduct(sid):
    form = AddUnlistedProductForm()
    if form.validate_on_submit():
        f = form.image_file.data
        filename = secure_filename(f.filename)
        image_path = os.path.join('app/static/images/', filename)
        f.save(image_path)
        #image_path2 = "../static/images/" + filename
        new_item = Inventory.add_unlisted_item(sid, form.name.data, form.description.data, form.category.data, filename, form.price.data, form.quantity.data)

        if new_item is False:
            flash('Error adding to inventory: Image file uploaded is likely not valid.')
            return redirect(url_for('inventory.addListedProduct', sid=sid))
        
        flash('Successfully added new unlisted item to inventory!')
        return redirect(url_for("inventory.addUnlistedProduct", sid=sid))
    return render_template('add_unlisted_product.html', title='Add Unlisted Product', form=form, sid=sid)

class AddListedProductForm(FlaskForm):
    pid = IntegerField('Product ID', validators=[InputRequired()])
    price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be >= $0")])
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=0, message="Quantity must be >= 0 units")])
    submit = SubmitField('Add Product')


@bp.route('/add-listed-Product/<sid>', methods=['GET','POST'])
def addListedProduct(sid):
    form = AddListedProductForm()
    if form.validate_on_submit():
        new_item = Inventory.add_listed_item(form.pid.data, sid, form.price.data, form.quantity.data)

        if new_item is False:
            flash('Error adding to inventory: Item is already in your inventory')
            return redirect(url_for('inventory.addListedProduct', sid=sid))

        flash('Successfully added new listed item to inventory!')
        return redirect(url_for("inventory.addListedProduct", sid=sid))
    return render_template('add_listed_product.html', title='Add Listed Product', form=form, sid=sid)

class RemoveInventoryForm(FlaskForm):
    confirm = SelectField('Confirm that you want to remove this product from inventory? (Y/N)', choices=["Yes", "No"])
    submit = SubmitField('Remove Inventory')

@bp.route('/remove-inventory/<sid>/<pid>', methods=['GET','POST'])
def removeInventory(sid, pid):
    #print("pid", pid)
    form = RemoveInventoryForm()
    confirmation = form.confirm.data
    if confirmation == "No":
        flash('You indicated that this item is NOT fulfilled.')
        return redirect(url_for("inventory.inventory", sid=sid))
    if confirmation == "Yes":
        Inventory.remove_item(sid, pid)
        flash('Successfully removed item from inventory!')
        return redirect(url_for("inventory.inventory", sid=sid))
    return render_template('remove_inventory.html', title='Remove from Inventory', form=form, inventory=inventory, sid=sid, pid=pid)


