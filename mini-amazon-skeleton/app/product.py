from pickle import TRUE
from flask import render_template, request
from flask_login import current_user
import datetime

from app.inventory import inventory
from app.models.inventory import Inventory

from .models.product import Product
from .models.inventory import Inventory

from app.models.review import Review

from flask import Blueprint
bp = Blueprint('product', __name__)

@bp.route('/product/<pid>', methods=['GET'])
def product(pid):
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


    return render_template("product.html", product=product, stock=stock, display_price=min_price, inventory=inventory, reviews = reviews)


@bp.route('/product/<pid>/<sid>', methods=['GET'])
def addToCart(pid, sid):
    product = Product.get(pid)
    listing = Inventory.get_item(pid, sid)
    # Do stuff to edit Cart
    return render_template("added_to_cart.html", product=product, listing = listing, quantity=request.form['quantity'])