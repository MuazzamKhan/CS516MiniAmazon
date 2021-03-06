from itertools import product
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, SelectField
from wtforms.validators import InputRequired, NumberRange, Length
from flask_babel import _, lazy_gettext as _l

from .models.seller_analytics import Product_Rank, Category_Rank, Inventory_Analytics, Seller_Review_Analytics, Product_Review_Analytics

from flask import Blueprint
bp = Blueprint('seller_analytics', __name__)

@bp.route('/seller-product-analytics/<sid>', methods=['GET'])
def sellerAnalytics(sid):
    top_products = Product_Rank.top_three_products(sid)
    bottom_products = Product_Rank.bottom_three_products(sid)
    top_categories = Category_Rank.top_three_categories(sid)
    bottom_categories = Category_Rank.bottom_three_categories(sid)
    all_categories = Category_Rank.all_categories(sid)
    return render_template("seller_analytics.html", 
    top_products=top_products, 
    bottom_products=bottom_products, 
    top_categories=top_categories, 
    bottom_categories=bottom_categories,
    all_categories = all_categories,
    all_categories_x = [row[0] for row in all_categories],
    all_categories_y = [row[1] for row in all_categories],
    sid=sid)

@bp.route('/seller-review-analytics/<sid>', methods=['GET'])
def sellerReviewAnalytics(sid):
    avg_seller_rating = Seller_Review_Analytics.avg_seller_rating(sid)
    num_seller_reviews = Seller_Review_Analytics.count_reviews(sid)
    seller_ratings_breakdown = Seller_Review_Analytics.seller_ratings_breakdown(sid)
    overall_product_rating = Product_Review_Analytics.overall_product_rating(sid)
    num_product_reviews = Product_Review_Analytics.count_reviews(sid)
    product_ratings_breakdown = Product_Review_Analytics.product_ratings_breakdown(sid)
    return render_template("seller_review_analytics.html",
    avg_seller_rating=avg_seller_rating,
    num_seller_reviews = num_seller_reviews,
    seller_ratings_breakdown = seller_ratings_breakdown,
    seller_ratings_x = [row[0] for row in seller_ratings_breakdown],
    seller_ratings_y = [row[1] for row in seller_ratings_breakdown],
    overall_product_rating=overall_product_rating,
    num_product_reviews=num_product_reviews,
    product_ratings_breakdown=product_ratings_breakdown,
    sid=sid)