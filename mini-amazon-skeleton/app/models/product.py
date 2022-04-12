from pickle import FALSE
from flask import current_app as app


class Product:
    def __init__(self, id, name, description, available, category, image_file):
        self.id = id
        self.name = name
        self.description = description
        self.available = available
        self.category = category
        self.image_file = image_file

    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, name, description, available, category, image_file
            FROM Products
            WHERE id = :id
            ''',
            id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
            SELECT id, name, description, available, category, image_file
            FROM Products
            WHERE available = :available
            ''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def add(name, description, category, image_file):
        rows = app.db.execute('''
            INSERT INTO Products(name, description, available, category, image_file)
            VALUES(:name, :description, TRUE, :category, :image_file)
            RETURNING id
        ''',
        name=name,
        description=description,
        category=category,
        image_file=image_file)

        #print("product rows:", rows)
            
        id = rows[0][0]

        return id if rows else None

    @staticmethod
    def addToCart(id, pid, sid, quantity, price):
        rows = app.db.execute('''
            SELECT quantity
            FROM Cart
            WHERE id = :id AND pid = :pid AND sid = :sid
            ''', id = id, pid = pid, sid = sid)

        if len(rows)>0:
            # app.db.execute('''
            #     DELETE FROM Cart
            #     WHERE id = :id AND pid = :pid AND sid = :sid
            #     ''', id = id, pid = pid, sid = sid)
            return False

        app.db.execute('''
            INSERT INTO Cart(id, pid, sid, quantity, price)
            VALUES(:id, :pid, :sid, :quantity, :price)
            RETURNING id
        ''',
        id=id,
        pid=pid,
        sid=sid,
        quantity=quantity,
        price=price)

        return True