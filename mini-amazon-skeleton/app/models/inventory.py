from flask import current_app as app
from flask_login import current_user

from .models.product import Product


class Inventory:
    def __init__(this, pid, sid, price, quantity):
        this.pid = pid
        this.sid = sid
        this.price = price
        this.quantity = quantity
    
    @staticmethod
    def get_item(pid, sid):
        rows = app.db.execute('''
        SELECT pid, sid, price, quantity
        FROM Inventory
        WHERE pid=:pid AND sid=:sid
        ''',
        pid=pid,
        sid=sid)
        if rows:
            return Inventory(*(rows[0]))
        else:
            None


    @staticmethod
    def get_with_sid(sid):
        rows = app.db.execute('''
        SELECT pid, sid, price, quantity
        FROM Inventory 
        WHERE sid=:sid
        ''',
        sid=sid)
        if rows:
            return [Inventory(*row) for row in rows]
        else: 
            None


    @staticmethod
    def get_with_pid(pid):
        rows = app.db.execute('''
        SELECT pid, sid, price, quantity
        FROM Inventory 
        WHERE pid=:pid
        ''',
        pid=pid)
        if rows:
            return [Inventory(*row) for row in rows]
        else: 
            None

    @staticmethod
    def get_with_price(floor, ceiling):
        rows = app.db.execute('''
        SELECT pid, sid, price, quantity
        FROM Inventory 
        WHERE price>=:floor AND price<=:ceiling
        ''',
        floor=floor,
        ceiling=ceiling)
        if rows:
            return [Inventory(*row) for row in rows]
        else: 
            None



    @staticmethod
    def get_with_quantity(floor, ceiling):
        rows = app.db.execute('''
        SELECT pid, sid, price, quantity
        FROM Inventory 
        WHERE quantity>=:floor AND quantity<=:ceiling
        ''',
        floor=floor,
        ceiling=ceiling)
        if rows:
            return [Inventory(*row) for row in rows]
        else: 
            None


    @staticmethod
    def add_item(pid, sid, price, quantity):
    ###WILL NEED TO ADD A LINE TO ADD ITEM INTO PRODUCT TABLE: https://gitlab.oit.duke.edu/the-primary-keys-316/mini-amazon/-/blob/main/app/models/inventoryitem.py
        pid = Product.add()
        
        rows = app.db.execute('''
            INSERT INTO Inventory(pid, sid, price, quantity)
            VALUES(:pid, :sid, :price, :quantity)
        ''',
        pid=pid,
        sid=sid,
        price=price,
        quantity=quantity)

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

    
    @staticmethod
    def calc_unique_items(sid) : 
        num = app.db.execute('''
        SELECT COUNT(pid)
        FROM Inventory
        WHERE sid=:sid
        ''',
        sid = sid)
        return num


    @staticmethod
    def calc_total_quantity(sid) : 
        num = app.db.execute('''
        SELECT SUM(quantity)
        FROM Inventory
        WHERE sid=:sid
        ''',
        sid = sid)
        return num


    @staticmethod
    def calc_average_price(sid) : 
        num = app.db.execute('''
        SELECT AVG(price)
        FROM Inventory
        WHERE sid=:sid
        ''',
        sid = sid)
        return num

