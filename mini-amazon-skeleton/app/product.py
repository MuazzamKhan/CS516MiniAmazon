from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product

from flask import Blueprint
bp = Blueprint('product', __name__)

@bp.route('/product/<pid>', methods=['GET'])
def product(pid):
    product = Product.get(pid)
    if product == None:
        return "Error! No such product exists!"
    else:
        return render_template("product.html", product=product, general=product)