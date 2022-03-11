from flask import current_app as app
from flask_login import current_user


class Inventory:
    def __init__(self, seller_id, product_id, price, quantity):
            self.seller_id = seller_id
            self.product_id = product_id
            self.price = price
            self.quantity = quantity
    
     @staticmethod
    def get_item(product_id, seller_id):
        rows = app.db.execute('''
        SELECT product_id, seller_id, price, quantity
        FROM InventoryItem
        WHERE product_id = :product_id AND seller_id = :seller_id
        ''',
        product_id = product_id,
        seller_id = seller_id)
        return Inventory(*(rows[0])) if rows else None


    @staticmethod
    def get_by_seller(seller_id):
        rows = app.db.execute('''
        SELECT product_id, seller_id, price, quantity
        FROM Inventory 
        WHERE seller_id = :seller_id
        ''',
        seller_id=seller.id)
        return [Inventory(*row) for row in rows] if rows else None


    @staticmethod
    def get_by_product(product_id):
        rows = app.db.execute('''
        SELECT product_id, seller_id, price, quantity
        FROM Inventory 
        WHERE product_id = :product_id
        ''',
        product_id=product_id)
        return [Inventory(*row) for row in rows] if rows else None



    @staticmethod
    def add_item(product_id, seller_id, price, quantity):
    ###WILL NEED TO ADD A LINE TO ADD ITEM INTO PRODUCT TABLE: https://gitlab.oit.duke.edu/the-primary-keys-316/mini-amazon/-/blob/main/app/models/inventoryitem.py
        rows = app.db.execute('''
            INSERT INTO Inventory(product_id, seller_id, price, quantity)
            VALUES(:product_id, :seller_id, :price, :quantity)
            RETURNING product_id
        ''',
        product_id=product_id,
        seller_id=seller_id,
        price=price,
        quantity=quantity)
        return True if rows else False


    @staticmethod
    def remove_item(seller_id, product_id):
        rows = app.db.execute('''
            DELETE FROM Inventory
            WHERE product_id = :product_id
            AND seller_id = :seller_id
            RETURNING NULL
            ''',
            product_id = product_id,
            seller_id = seller_id)
        return True if rows else False


    @staticmethod
    def edit_quantity(product_id, seller_id, quantity):
        rows = app.db.execute('''
            UPDATE Inventory
            SET quantity = :quantity
            WHERE product_id = :product_id
            AND seller_id = :seller_id
            RETURNING quantity
        ''', 
        product_id = product_id,
        seller_id = seller_id,
        quantity = quantity)
        return rows


    @staticmethod
    def edit_price(product_id, seller_id, price):
        rows = app.db.execute('''
            UPDATE Inventory
            SET price = :price
            WHERE product_id = :product_id
            AND seller_id = :seller_id
            RETURNING price
        ''', 
        product_id = product_id, 
        seller_id = seller_id, 
        price = price)
        return rows

    
    @staticmethod
    def count_items_seller(seller_id) : 
        count = app.db.execute('''
        SELECT COUNT(seller_id)
        FROM Inventory
        WHERE seller_id= :seller_id
        ''',
        seller_id = seller_id) 
        return count

