from pickle import TRUE
from flask import render_template, request
from flask_login import current_user
import datetime

from app.inventory import inventory
from app.models.inventory import Inventory
from app.models.purchase import Purchase

from .models.product import Product
from .models.inventory import Inventory
from .models.cart import Cart
from .models.order import Order
from .models.user import User

from flask import Blueprint
bp = Blueprint('cart', __name__)

@bp.route('/cart', methods=['GET'])
def cart():
    cart_items = []

    if current_user.is_authenticated:
        cart_items = Cart.get_all(current_user.id)

        cart_total = 0

        for item in Cart.get_all_non_wishlist(current_user.id):
            cart_total += item.total
        
        return render_template("cart.html", cart_items=cart_items, cart_total=cart_total)

    return render_template("cart.html", cart_items=cart_items)

@bp.route('/cart/<pid>/<sid>', methods=['GET'])
def delete(pid, sid):
    Cart.delete_item(current_user.id, pid, sid)

    cart_items = Cart.get_all(current_user.id)

    cart_total = 0

    for item in Cart.get_all_non_wishlist(current_user.id):
            cart_total += item.total
        
    return render_template("cart.html", cart_items=cart_items, cart_total=cart_total)

@bp.route('/cart/wishlist/<pid>/<sid>', methods=['GET'])
def wishlist(pid, sid):
    Cart.wishlist_item(current_user.id, pid, sid)

    cart_items = Cart.get_all(current_user.id)

    cart_total = 0

    for item in Cart.get_all_non_wishlist(current_user.id):
            cart_total += item.total
        
    return render_template("cart.html", cart_items=cart_items, cart_total=cart_total)

@bp.route('/cart/unwishlist/<pid>/<sid>', methods=['GET'])
def unwishlist(pid, sid):
    Cart.unwishlist_item(current_user.id, pid, sid)

    cart_items = Cart.get_all(current_user.id)

    cart_total = 0

    for item in Cart.get_all_non_wishlist(current_user.id):
            cart_total += item.total
        
    return render_template("cart.html", cart_items=cart_items, cart_total=cart_total)

@bp.route('/cart/order', methods=['GET'])
def order():
    cart_items = Cart.get_all(current_user.id)
    cart_nonwishlist = Cart.get_all_non_wishlist(current_user.id)

    order_cost = 0
    for item in cart_nonwishlist:
        order_cost += item.total

        if User.get_balance(current_user.id) < order_cost: # insufficient funds
            message = "Insufficient Funds!"
            return render_template("cart.html", cart_items=cart_items, cart_total=order_cost, message = message)

        stock = Inventory.get_item(item.pid, item.sid).quantity
        if stock<item.quantity: # insufficient stock
            message = "Not enough stock for product " + item.pid
            return render_template("cart.html", cart_items=cart_items, cart_total=order_cost, message = message)

    oid = Order.add_to_order()

    for item in cart_nonwishlist:

        Purchase.add_to_purchases(item, oid)
        User.update_balance(current_user.id, 0, item.total)

        Cart.delete_item(current_user.id, item.pid, item.sid)

        new_quantity = Inventory.get_item(item.pid, item.sid).quantity - item.quantity
        Inventory.edit_quantity(item.pid, item.sid, new_quantity)

    cart_items = Cart.get_all(current_user.id)
    cart_total = 0
    for item in Cart.get_all_non_wishlist(current_user.id):
            cart_total += item.total
    return render_template("cart.html", cart_items=cart_items, cart_total=cart_total)

@bp.route('/cart/edit/<pid>/<sid>', methods=['GET'])
def edit(pid, sid):
    cart_item = Cart.get_one(current_user.id, pid, sid)
    stock = Inventory.get_item(pid, sid).quantity

    return render_template("edit_cart.html", item = cart_item, stock = stock)

@bp.route('/cart/editquantity/<pid>/<sid>', methods=['POST','GET'])
def editCart(pid, sid):
    quantity = request.args['quantity']
    Cart.edit_item(current_user.id, pid, sid, quantity)
    
    cart_total = 0
    cart_items = Cart.get_all(current_user.id)
    for item in Cart.get_all_non_wishlist(current_user.id):
            cart_total += item.total
        
    return render_template("cart.html", cart_items=cart_items, cart_total=cart_total)