from flask import current_app as app

from .seller import Seller
from .product import Product

class Cart:
    def __init__(self, id, pid, sid, quantity, price, wishlist):
        self.id = id
        self.pid = pid
        self.sid = sid
        self.quantity = quantity
        self.price = price
        self.wishlist = wishlist
        self.total = quantity*price
        self.sellerName = Seller.getNameFromSid(sid)
        self.productName = Product.get(pid).name

    @staticmethod
    def get_one(id, pid, sid):
        rows = app.db.execute('''
            SELECT id, pid, sid, quantity, price, wishlist
            FROM Cart
            WHERE id = :id AND pid = :pid AND sid = :sid
            ''', 
            id = id,
            pid = pid,
            sid = sid)

        return Cart(*(rows[0])) 

    @staticmethod
    def get_all(id):
        rows = app.db.execute('''
            SELECT id, pid, sid, quantity, price, wishlist
            FROM Cart
            WHERE id = :id
            ''', id = id)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_all_non_wishlist(id):
        rows = app.db.execute('''
            SELECT id, pid, sid, quantity, price, wishlist
            FROM Cart
            WHERE id = :id AND wishlist = FALSE
            ''', id = id)
        return [Cart(*row) for row in rows]

    # @staticmethod
    # def get_all_wishlist(id):
    #     rows = app.db.execute('''
    #         SELECT id, pid, sid, quantity, price, wishlist
    #         FROM Cart
    #         WHERE id = :id AND wishlist = TRUE
    #         ''', id = id)
    #     return [Cart(*row) for row in rows]

    @staticmethod
    def delete_item(id, pid, sid):
        app.db.execute('''
            DELETE FROM Cart
            WHERE id=:id AND pid=:pid AND sid=:sid
            ''', 
            id = id,
            pid = pid,
            sid = sid)

    @staticmethod
    def edit_item(id, pid, sid, quantity):
        app.db.execute('''
            UPDATE Cart
            SET quantity = :quantity
            WHERE pid = :pid
            AND sid = :sid
            AND id = :id
            ''', 
            id = id,
            pid = pid,
            sid = sid,
            quantity = quantity)

    @staticmethod
    def wishlist_item(id, pid, sid):
        app.db.execute('''
            UPDATE Cart
            SET wishlist = TRUE
            WHERE pid = :pid
            AND sid = :sid
            AND id = :id
            ''', 
            id = id,
            pid = pid,
            sid = sid,
            )

    @staticmethod
    def unwishlist_item(id, pid, sid):
        app.db.execute('''
            UPDATE Cart
            SET wishlist = FALSE
            WHERE pid = :pid
            AND sid = :sid
            AND id = :id
            ''', 
            id = id,
            pid = pid,
            sid = sid,
            )