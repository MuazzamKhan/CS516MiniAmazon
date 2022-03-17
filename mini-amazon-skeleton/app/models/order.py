from os import name
from flask import current_app as app

class Order:
    def __init__(self, id, uid, pid, sid, product_name, price, quantity, placed_datetime, completed_status, completion_datetime, address):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.product_name = product_name,
        self.price = price
        self.quantity = quantity
        self.placed_datetime = placed_datetime
        self.completed_status = completed_status
        self.completion_datetime = completion_datetime
        self.address = address
    
    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
        SELECT PUR.id, PUR.uid, PUR.pid, PUR.sid, PROD.name AS product_name, PUR.price, PUR.quantity, PUR.placed_datetime, PUR.completed_status, PUR.completion_datetime, BUY.address
        FROM Purchases PUR, Users BUY, Products PROD
        WHERE PUR.uid = BUY.id
        AND PUR.pid = PROD.id
        AND PUR.uid=:uid
        ORDER BY placed_datetime DESC
        ''',
        uid=uid)
        if rows:
            return [Order(*row) for row in rows]
        else: 
            None

    @staticmethod
    def get_by_sid(sid):
        rows = app.db.execute('''
        SELECT PUR.id, PUR.uid, PUR.pid, PUR.sid, PROD.name AS product_name, PUR.price, PUR.quantity, PUR.placed_datetime, PUR.completed_status, PUR.completion_datetime, BUY.address
        FROM Purchases PUR, Users BUY, Products PROD
        WHERE PUR.uid = BUY.id
        AND PUR.pid = PROD.id
        AND PUR.sid=:sid
        ORDER BY placed_datetime DESC
        ''',
        sid=sid)
        if rows:
            return [Order(*row) for row in rows]
        else: 
            None

    @staticmethod
    def get_by_id(id):
        rows = app.db.execute('''
        SELECT PUR.id, PUR.uid, PUR.pid, PUR.sid, PROD.name AS product_name, PUR.price, PUR.quantity, PUR.placed_datetime, PUR.completed_status, PUR.completion_datetime, BUY.address
        FROM Purchases PUR, Users BUY, Products PROD
        WHERE PUR.uid = BUY.id
        AND PUR.pid = PROD.id
        AND PUR.id=:id
        ORDER BY placed_datetime DESC
        ''',
        id=id)
        if rows:
            return [Order(*row) for row in rows]
        else: 
            None

    @staticmethod
    def get_by_sid_status(sid, completed_status):
        rows = app.db.execute('''
        SELECT PUR.id, PUR.uid, PUR.pid, PUR.sid, PROD.name AS product_name, PUR.price, PUR.quantity, PUR.placed_datetime, PUR.completed_status, PUR.completion_datetime, BUY.address
        FROM Purchases PUR, Users BUY, Products PROD
        WHERE PUR.uid = BUY.id
        AND PUR.pid = PROD.id
        AND PUR.sid=:sid
        AND completed_status=:completed_status
        ORDER BY placed_datetime DESC
        ''',
        sid=sid,
        completed_status=completed_status)
        if rows:
            return [Order(*row) for row in rows]
        else: 
            None

    def get_by_uid_status(uid):
        rows = app.db.execute('''
        SELECT PUR.id, PUR.uid, PUR.pid, PUR.sid, PROD.name AS product_name, PUR.price, PUR.quantity, PUR.placed_datetime, PUR.completed_status, PUR.completion_datetime, BUY.address
        FROM Purchases PUR, Users BUY, Products PROD
        WHERE PUR.uid = BUY.id
        AND PUR.pid = PROD.id
        AND PUR.uid=:uid
        AND completed_status=:completed_status
        ORDER BY placed_datetime DESC
        ''',
        uid=uid,
        completed_status=completed_status)
        if rows:
            return [Order(*row) for row in rows]
        else: 
            None

            
    @staticmethod
    def mark_fulfilled(id, pid):
        rows = app.db.execute('''
            UPDATE Purchases
            SET completed_status = TRUE
            AND completion_datetime = CURRENT_TIMESTAMP
            WHERE pid=:pid
            AND id=:id
        ''', 
        id=id,
        pid=pid)
        if rows:
            return True
        else: 
            return False