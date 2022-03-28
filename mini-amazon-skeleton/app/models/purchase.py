from flask import current_app as app
from flask_login import current_user

from .product import Product

class Purchase:
    def __init__(self, oid, uid, product, sid, sfirstname, slastname, price, quantity, completed_status, time_purchased):
        self.oid = oid
        self.uid = uid
        self.product = product
        self.sid = sid
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
    def add_to_purchases(item, oid):
        app.db.execute('''
            INSERT INTO Purchases(oid, pid, sid, price, quantity)
            VALUES(:oid, :pid, :sid, :price, :quantity)
        ''',
        oid=oid,
        pid=item.pid,
        sid=item.sid,
        price=item.price,
        quantity=item.quantity
        )

    @staticmethod
    def get_all_by_uid_since(uid, start_date, end_date, product='%', seller_firstname='%', seller_lastname='%'):
        rows = app.db.execute('''
SELECT oid, o.bid, pro.name, sid, u.firstname, u.lastname, price, quantity, p.completed_status, p.completion_datetime
FROM Purchases AS p, Orders AS o, Products AS pro, Users AS u
WHERE o.bid = :uid
    AND o.id = p.oid 
    AND pro.id = p.pid 
    AND u.id = sid
    AND p.completion_datetime >= :start_date
    AND p.completion_datetime <= :end_date
    AND LOWER(pro.name) LIKE :product
    AND ( ( LOWER(u.firstname) LIKE :firstname AND LOWER(u.lastname) LIKE :lastname ) OR ( LOWER(u.firstname) LIKE :lastname AND LOWER(u.lastname) LIKE :firstname ) )
ORDER BY p.completion_datetime DESC
''',
                              uid=uid,
                              start_date=start_date,
                              end_date=end_date,
                              product=product,
                              firstname=seller_firstname,
                              lastname=seller_lastname)
        
        return [Purchase(*row) for row in rows]

