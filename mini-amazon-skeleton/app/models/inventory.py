from flask import current_app as app
from flask_login import current_user

from .product import Product
from .seller import Seller


class Inventory:
    def __init__(this, pid, category, name, sid, price, quantity, stock):
        this.pid = pid
        this.category = category
        this.name = name
        this.sid = sid
        this.price = price
        this.quantity = quantity
        this.stock = stock
        this.sellerName = Seller.getNameFromSid(sid)
    
    @staticmethod
    def get_item(pid, sid):
        rows = app.db.execute('''
        SELECT pid, prod.category, prod.name AS name, sid, price, quantity, CASE
            WHEN quantity < 6 THEN 'Low'
            WHEN quantity < 20 THEN 'Moderate'
            ELSE 'High'
        END AS stock
        FROM Inventory inv, Products prod
        WHERE inv.pid = prod.id
        AND pid=:pid
        AND sid=:sid
        ''',
        pid=pid,
        sid=sid)
        return Inventory(*(rows[0]))

    @staticmethod
    def get_with_sid(sid):
        rows = app.db.execute('''
        SELECT pid, prod.category, prod.name AS name, sid, price, quantity, CASE
            WHEN quantity < 6 THEN 'Low'
            WHEN quantity < 20 THEN 'Moderate'
            ELSE 'High'
        END AS stock
        FROM Inventory inv, Products prod
        WHERE inv.pid = prod.id
        AND inv.sid=:sid
        ORDER BY pid
        ''',
        sid=sid)
        return [Inventory(*row) for row in rows]


    @staticmethod
    def get_with_pid(pid):
        rows = app.db.execute('''
        SELECT pid, prod.category, prod.name AS name, sid, price, quantity, CASE
            WHEN quantity < 6 THEN 'Low'
            WHEN quantity < 20 THEN 'Moderate'
            ELSE 'High'
        END AS stock
        FROM Inventory inv, Products prod
        WHERE inv.pid = prod.id
        AND pid=:pid
        ''',
        pid=pid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_with_price(floor, ceiling):
        rows = app.db.execute('''
        SELECT pid, prod.category, prod.name AS name, sid, price, quantity, CASE
            WHEN quantity < 6 THEN 'Low'
            WHEN quantity < 20 THEN 'Moderate'
            ELSE 'High'
        END AS stock
        FROM Inventory inv, Products prod
        WHERE inv.pid = prod.id
        AND price>=:floor AND price<=:ceiling
        ''',
        floor=floor,
        ceiling=ceiling)
        return [Inventory(*row) for row in rows]



    @staticmethod
    def get_with_quantity(floor, ceiling):
        rows = app.db.execute('''
        SELECT pid, prod.category, prod.name AS name, sid, price, quantity, CASE
            WHEN quantity < 6 THEN 'Low'
            WHEN quantity < 20 THEN 'Moderate'
            ELSE 'High'
        END AS stock
        FROM Inventory inv, Products prod
        WHERE inv.pid = prod.id 
        AND quantity>=:floor AND quantity<=:ceiling
        ''',
        floor=floor,
        ceiling=ceiling)
        return [Inventory(*row) for row in rows]


    @staticmethod
    def add_unlisted_item(sid, name, description, category, image_file, price, quantity):
        
        
        #print(pid)
        
        try:
            pid = Product.add(name, description, category, image_file)
            rows = app.db.execute('''
                INSERT INTO Inventory(pid, sid, price, quantity)
                VALUES(:pid, :sid, :price, :quantity)
            ''',
            pid=pid,
            sid=sid,
            price=price,
            quantity=quantity)
        except Exception:
            rows = None

        #print("rows: ", rows)

        if rows:
            return True
        else: 
            return False

    
    @staticmethod
    def add_listed_item(pid, sid, price, quantity):
        try: 
            rows = app.db.execute('''
            INSERT INTO Inventory(pid, sid, price, quantity)
            VALUES(:pid, :sid, :price, :quantity)
            ''',
            pid=pid,
            sid=sid,
            price=price,
            quantity=quantity)
        except Exception:
            rows = None
            
        if rows:
            return True
        else: 
            return False


    @staticmethod
    def remove_item(sid, pid):
        rows = app.db.execute('''
            DELETE FROM Inventory
            WHERE pid = :pid
            AND sid = :sid
            ''',
            pid = pid,
            sid = sid)
        if rows:
            return True
        else: 
            return False


    @staticmethod
    def edit_quantity(pid, sid, quantity):
        rows = app.db.execute('''
            UPDATE Inventory
            SET quantity = :quantity
            WHERE pid = :pid
            AND sid = :sid
        ''', 
        pid = pid,
        sid = sid,
        quantity = quantity)
        if rows:
            return True
        else: 
            return False


    @staticmethod
    def edit_price(pid, sid, price):
        rows = app.db.execute('''
            UPDATE Inventory
            SET price = :price
            WHERE pid = :pid
            AND sid = :sid
        ''', 
        pid = pid, 
        sid = sid, 
        price = price)
        if rows:
            return True
        else: 
            return False