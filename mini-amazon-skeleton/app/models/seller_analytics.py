from os import name
from flask import current_app as app

class Product_Rank:
    def __init__(self, pid, product_name, count):
        self.pid = pid
        self.product_name = product_name
        self.count = count
        
    @staticmethod
    def top_three_products(sid):
        rows = app.db.execute('''
        SELECT PUR.pid, PROD.name AS product_name, SUM(PUR.quantity) AS count
        FROM Purchases PUR, Products PROD
        WHERE PUR.pid = PROD.id
        AND PUR.sid=:sid
        GROUP BY PUR.pid, product_name
        ORDER BY count DESC
        LIMIT 3
        ''',
        sid=sid)

        if rows:
            return [Product_Rank(*row) for row in rows]
        else: 
            None

    @staticmethod
    def bottom_three_products(sid):
        rows = app.db.execute('''
        SELECT PUR.pid, PROD.name AS product_name, SUM(PUR.quantity) AS count
        FROM Purchases PUR, Products PROD
        WHERE PUR.pid = PROD.id
        AND PUR.sid=:sid
        GROUP BY PUR.pid, product_name
        ORDER BY count ASC
        LIMIT 3
        ''',
        sid=sid)

        if rows:
            return [Product_Rank(*row) for row in rows]
        else: 
            None

class Category_Rank:

    def __init__(self, category, count):
        self.category = category
        self.count = count

    @staticmethod
    def top_three_categories(sid):
        rows = app.db.execute('''
        SELECT PROD.category AS category, COUNT(PUR.quantity) AS count
        FROM Purchases PUR, Products PROD
        WHERE PUR.pid = PROD.id
        AND PUR.sid=:sid
        GROUP BY PROD.category
        ORDER BY count DESC
        LIMIT 3
        ''',
        sid=sid)

        if rows:
            return [Category_Rank(*row) for row in rows]
        else: 
            None

    @staticmethod
    def bottom_three_categories(sid):
        rows = app.db.execute('''
        SELECT PROD.category AS category, COUNT(PUR.quantity) AS count
        FROM Purchases PUR, Products PROD
        WHERE PUR.pid = PROD.id
        AND PUR.sid=:sid
        GROUP BY PROD.category
        ORDER BY count ASC
        LIMIT 3
        ''',
        sid=sid)

        if rows:
            return [Category_Rank(*row) for row in rows]
        else: 
            None

    @staticmethod
    def all_categories(sid):
        rows = app.db.execute('''
        SELECT PROD.category AS category, COUNT(PUR.quantity) AS count
        FROM Purchases PUR, Products PROD
        WHERE PUR.pid = PROD.id
        AND PUR.sid=:sid
        GROUP BY PROD.category
        ORDER BY count DESC
        ''',
        sid=sid)

        if rows:
            return rows
        else: 
            None

class Inventory_Analytics:
    def __init__(this, pid, sid, price, quantity):
        this.pid = pid
        this.sid = sid
        this.price = price
        this.quantity = quantity


    @staticmethod
    def calc_unique_items(sid) : 
        num = app.db.execute('''
        SELECT COUNT(pid)
        FROM Inventory
        WHERE sid=:sid
        ''',
        sid = sid)
        if num[0][0] == None or num[0][0] == 0:
            return None
        else:
            return num[0][0]


    @staticmethod
    def calc_total_quantity(sid) : 
        num = app.db.execute('''
        SELECT SUM(quantity)
        FROM Inventory
        WHERE sid=:sid
        ''',
        sid = sid)
        if num[0][0] == None or num[0][0] == 0:
            return None
        else:
            return num[0][0]


    @staticmethod
    def calc_average_price(sid) : 
        num = app.db.execute('''
        SELECT AVG(price)
        FROM Inventory
        WHERE sid=:sid
        ''',
        sid = sid)
        if num[0][0] == None:
            return None
        else:
            return round(num[0][0], 2)


    @staticmethod
    def inventory_low(pid, sid):
        rows = app.db.execute('''
        SELECT quantity
        FROM Inventory
        WHERE pid=:pid AND sid=:sid
        ''',
        pid=pid,
        sid=sid)

        if rows[0][0] == None:
            return None

        if rows[0][0] <= 5:
            return "Low in Stock"
        elif rows[0][0] <= 20:
            return "Moderate in Stock"
        else:
            return "High in Stock"

class Seller_Review_Analytics:
    def __init__(this, sid, bid, count, rating):
        this.sid = sid
        this.bid = bid
        this.count = count
        this.rating = rating

    @staticmethod
    def avg_seller_rating(sid):
        num = app.db.execute('''
        SELECT ROUND(AVG(rating),2)
        FROM Reviews_sellers
        WHERE sid=:sid
        ''', 
        sid=sid)

        if num == None:
            return num
        else:
            return num[0][0]

    @staticmethod
    def count_reviews(sid):
        num = app.db.execute('''
        SELECT COUNT(uid)
        FROM Reviews_sellers
        WHERE sid=:sid
        ''',
        sid=sid)

        if num == None:
            return num
        else:
            return num[0][0]

    @staticmethod
    def seller_ratings_breakdown(sid):
        rows = app.db.execute('''
        SELECT rating, COUNT(uid)
        FROM Reviews_sellers
        WHERE sid=:sid
        GROUP BY rating
        ''',
        sid = sid)

        if rows:
            return rows
        else: 
            None

class Product_Review_Analytics:
    def __init__(this, pid, name, count, rating):
        this.pid = pid
        this.name = name
        this.count = count
        this.rating = rating

    @staticmethod
    def overall_product_rating(sid):
        num = app.db.execute('''
        SELECT ROUND(AVG(REV.rating),2)
        FROM Reviews REV, Products PROD, Inventory INV
        WHERE REV.pid = PROD.id
        AND INV.pid = PROD.id
        AND INV.sid=:sid
        ''',
        sid=sid)

        if num == None:
            return num
        else:
            return num[0][0]

    @staticmethod
    def count_reviews(sid):
        num = app.db.execute('''
        SELECT COUNT(REV.rating)
        FROM Reviews REV, Products PROD, Inventory INV
        WHERE REV.pid = PROD.id
        AND INV.pid = PROD.id
        AND INV.sid=:sid
        ''',
        sid=sid)

        if num == None:
            return num
        else:
            return num[0][0]

    @staticmethod
    def product_ratings_breakdown(sid):
        rows = app.db.execute('''
        SELECT REV.pid, PROD.name, COUNT(REV.rating) as count, ROUND(AVG(REV.rating), 2) AS rating
        FROM Reviews REV, Products PROD, Inventory INV
        WHERE REV.pid = PROD.id
        AND INV.pid = PROD.id
        AND INV.sid=:sid
        GROUP BY REV.pid, PROD.name
        ''',
        sid=sid)

        if rows == None:
            return rows
        else:
            return rows