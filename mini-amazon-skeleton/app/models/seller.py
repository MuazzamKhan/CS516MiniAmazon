from datetime import datetime
from os import name
from flask import current_app as app
from flask_login import current_user

class Seller:
    def __init__(self, sid):
        self.sid = sid


    @staticmethod
    def isSeller(sid):
        rows = app.db.execute('''
            SELECT *
            FROM Sellers
            WHERE id=:sid
        ''',
        sid=sid
        )

        if rows:
            return True
        else: 
            return False
    