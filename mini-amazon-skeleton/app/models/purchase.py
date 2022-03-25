from flask import current_app as app

from .product import Product

class Purchase:
    def __init__(self, oid, uid, product, sfirstname, slastname, price, quantity, completed_status, time_purchased):
        self.oid = oid
        self.uid = uid
        self.product = product
        self.sname = sfirstname + " " + slastname
        self.time_purchased = time_purchased
        self.quantity = quantity
        self.price = price 
        self.completed_status = "Yes" if completed_status else "No"
        
    
    """
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None
    """

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT oid, o.bid, pro.name, u.firstname, u.lastname, price, quantity, p.completed_status, p.completion_datetime
FROM Purchases AS p, Orders AS o, Products AS pro, Users AS u
WHERE o.bid = :uid
    AND o.id = p.oid 
    AND pro.id = p.pid 
    AND u.id = sid
    AND p.completion_datetime >= :since
ORDER BY p.completion_datetime DESC
''',
                              uid=uid,
                              since=since)

        return [Purchase(*row) for row in rows]


