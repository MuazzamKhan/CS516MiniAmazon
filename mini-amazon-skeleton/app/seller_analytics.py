
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, SelectField
from wtforms.validators import InputRequired, NumberRange, Length
from flask_babel import _, lazy_gettext as _l

from .models.seller_analytics import Product_Rank, Category_Rank, Inventory_Analytics

from flask import Blueprint
bp = Blueprint('seller_analytics', __name__)

@bp.route('/seller-analytics/<sid>', methods=['GET'])
def sellerAnalytics(sid):
    top_products = Product_Rank.top_three_products(sid)
    bottom_products = Product_Rank.bottom_three_products(sid)
    top_categories = Category_Rank.top_three_categories(sid)
    bottom_categories = Category_Rank.bottom_three_categories(sid)
    all_categories = Category_Rank.all_categories(sid)
    unique_inventory = Inventory_Analytics.calc_unique_items(sid)
    total_inventory = Inventory_Analytics.calc_total_quantity(sid)
    avg_price_inventory = Inventory_Analytics.calc_average_price(sid)
    return render_template("seller_analytics.html", 
    top_products=top_products, 
    bottom_products=bottom_products, 
    top_categories=top_categories, 
    bottom_categories=bottom_categories,
    all_categories = all_categories,
    all_categories_x = [row[0] for row in all_categories],
    all_categories_y = [row[1] for row in all_categories],
    total_inventory=total_inventory, 
    unique_inventory=unique_inventory, 
    avg_price_inventory=avg_price_inventory, 
    sid=sid)