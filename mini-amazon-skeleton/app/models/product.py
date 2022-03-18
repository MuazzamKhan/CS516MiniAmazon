from flask import current_app as app


class Product:
    def __init__(self, id, name, price, available):
        self.id = id
        self.name = name
        self.price = price
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def add(sid, name, description, price):
        rows = app.db.execute('''
            INSERT INTO Products(sid, name, description, price, available)
            VALUES(:sid, :name, :description, :price, TRUE)
            RETURNING id
        ''',
        sid=sid,
        name=name,
        description=description,
        price=price)
            
        id = rows[0][0]

        return id if rows else None
