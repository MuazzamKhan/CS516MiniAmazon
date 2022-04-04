from flask import current_app as app
from flask_login import current_user

from .product import Product

class Purchase:
    def __init__(self, oid, uid, sid, sfirstname, slastname, price, quantity, completed_status, time_purchased):
        self.oid = oid
        self.uid = uid
        self.sid = sid
        self.sname = sfirstname + " " + slastname
        self.time_purchased = "NA (not completed)" if time_purchased == None else time_purchased
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
    def get_all_by_uid_since(uid, start_date, end_date, quantity=-1, seller_firstname='%', seller_lastname='%'):
        
        quantity_check = ""
        if quantity >= 0:
            quantity_check = "WHERE total_quantity = %d" % quantity
        
        query = "WITH subquery AS (" \
                    "SELECT oid, o.bid, sid, u.firstname, u.lastname, SUM(price) AS total_price, SUM(quantity) AS total_quantity, o.completed_status, o.completion_datetime " \
                    "FROM Purchases AS p, Orders AS o, Users AS u " \
                    "WHERE o.bid = :uid " \
                        "AND o.id = p.oid " \
                        "AND u.id = sid " \
                        "AND ( ( o.completion_datetime >= :start_date AND o.completion_datetime <= :end_date ) OR o.completion_datetime IS NULL )" \
                        "AND ( ( LOWER(u.firstname) LIKE :firstname AND LOWER(u.lastname) LIKE :lastname ) OR ( LOWER(u.firstname) LIKE :lastname AND LOWER(u.lastname) LIKE :firstname ) ) " \
                "GROUP BY oid, o.bid, sid, u.firstname, u.lastname, o.completed_status, o.completion_datetime ) "\
                "SELECT * "\
                "FROM subquery "\
                "%s ORDER BY completion_datetime DESC " % (quantity_check)
        rows = app.db.execute(query,
                              uid=uid,
                              start_date=start_date,
                              end_date=end_date,
                              firstname=seller_firstname,
                              lastname=seller_lastname)
        
        return [Purchase(*row) for row in rows]

