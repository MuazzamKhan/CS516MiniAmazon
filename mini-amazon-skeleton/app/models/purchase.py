from flask import current_app as app

from .product import Product

class Purchase:
    def __init__(self, id, uid, pid, sid, time_purchased, quantity, price, completed_status):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.time_purchased = time_purchased
        self.quantity = quantity
        this.price = price 
        this.completed_status = completed_status

        product = Product.get(pid)
        self.pname = product.name

        self.sname = ""

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, completion_datetime, quantity, price, completed_status
FROM Purchases
WHERE uid = :uid
AND completion_datetime >= :since
ORDER BY completion_datetime DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]


