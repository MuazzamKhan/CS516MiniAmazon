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
        return num[0][0]


    @staticmethod
    def calc_total_quantity(sid) : 
        num = app.db.execute('''
        SELECT SUM(quantity)
        FROM Inventory
        WHERE sid=:sid
        ''',
        sid = sid)
        return num[0][0]


    @staticmethod
    def calc_average_price(sid) : 
        num = app.db.execute('''
        SELECT AVG(price)
        FROM Inventory
        WHERE sid=:sid
        ''',
        sid = sid)
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

        if rows[0][0] <= 5:
            return "Low in Stock"
        elif rows[0][0] <= 20:
            return "Moderate in Stock"
        else:
            return "High in Stock"

