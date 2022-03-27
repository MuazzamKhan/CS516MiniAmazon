from os import name
from flask import current_app as app

class Order:
    def __init__(self, id, uid, pid, sid, product_name, price, quantity, placed_datetime, completed_status, completion_datetime, address):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.placed_datetime = placed_datetime
        self.completed_status = completed_status
        self.completion_datetime = completion_datetime
        self.address = address
        self.count = count
    
    @staticmethod
    def get_by_bid(bid):
        rows = app.db.execute('''
        SELECT ORD.id, ORD.bid, PUR.pid, PROD.sid, PROD.name AS product_name, PUR.price, PUR.quantity, ORD.placed_datetime, PUR.completed_status, PUR.completion_datetime, ORD.address
        FROM Orders ORD, Purchases PUR, Products PROD
        WHERE ORD.id = PUR.oid 
        AND PUR.pid = PROD.id
        AND ORD.bid=:bid
        ORDER BY ORD.placed_datetime DESC
        ''',
        bid=bid)
        if rows:
            return [Order(*row) for row in rows]
        else: 
            None

    @staticmethod
    def get_by_sid(sid):
        rows = app.db.execute('''
        SELECT ORD.id, ORD.bid, PUR.pid, PUR.sid, PROD.name AS product_name, PUR.price, PUR.quantity, ORD.placed_datetime, PUR.completed_status, PUR.completion_datetime, ORD.address
        FROM Orders ORD, Purchases PUR, Products PROD
        WHERE ORD.id = PUR.oid 
        AND PUR.pid = PROD.id
        AND PUR.sid=:sid
        ORDER BY ORD.placed_datetime DESC
        ''',
        sid=sid)
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
    def item_fulfilled(oid, pid):
        item_status = app.db.execute('''
            SELECT completed_status
            FROM Purchases
            WHERE pid=:pid
            AND oid=:oid
        ''', 
        oid=oid,
        pid=pid)

        print("oid = ", oid)

        #print("item status = ", item_status)

        print("item status = ", item_status[0][0])

        if item_status[0][0] == False:
            rows = app.db.execute('''
                UPDATE Purchases
                SET completed_status = TRUE, completion_datetime = CURRENT_TIMESTAMP
                WHERE pid=:pid
                AND oid=:oid
            ''', 
            oid=oid,
            pid=pid)
        
            return True
        else:
            return False

    @staticmethod
    def all_fulfilled_check(oid):

        print("oid = ", oid)

        all_items_status = app.db.execute('''
            SELECT completed_status
            FROM Purchases
            WHERE oid=:oid
        ''', 
        oid=oid)

        print("all_items_status = ", all_items_status)

        order_status = True

        for status in all_items_status:
            if status[0] == False:
                order_status = False
        
        print("order_status_final", order_status)
        
        if order_status == True:
            rows = app.db.execute('''
                UPDATE Orders
                SET completed_status = TRUE, completion_datetime = CURRENT_TIMESTAMP
                WHERE id=:oid
            ''', 
            oid=oid)
            return True

        else:
            return False



            
