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
    
    @staticmethod
    def update_receive_notification(sid, receive_notification):
        rows = app.db.execute('''
            UPDATE Sellers
            SET receive_notification = :receive_notification
            WHERE id=:sid
            RETURNING id
        ''',
        sid=sid,
        receive_notification=receive_notification
        )
        
        if len(rows[0]) > 0:
            if rows[0][0] == sid:
                return True
        else:
            return False

    @staticmethod
    def get_if_receive_notification(sid):
        rows = app.db.execute('''
            SELECT receive_notification
            FROM Sellers
            WHERE id=:sid
        ''',
        sid=sid
        )
        # if it is not a seller
        if len(rows) == 0:
            return False
        else:
            return rows[0][0]

    @staticmethod
    def getNameFromSid(sid):
        rows = app.db.execute('''
            SELECT *
            FROM Users
            WHERE id=:sid
        ''',
        sid=sid
        )

        return rows[0][3] + " " + rows[0][4][0] + "."


    
    @staticmethod
    def beSeller(id):
        try:
            sid = app.db.execute('''
            INSERT INTO Sellers(id)
            VALUES(:id)
            RETURNING id
            ''',
            id=id)
        except:
            return False

        return sid