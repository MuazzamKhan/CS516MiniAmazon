from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
    

    def set_profile(self, email, firstname, lastname, address):
        self.email = email 
        self.firstname = firstname
        self.lastname = lastname
        self.address = address

    @staticmethod
    def check_password(email, password):
        rows = app.db.execute("""
select password, id, email, firstname, lastname
from users
where email = :email
""",
                              email=email)
        
        if not rows:  # email not found
            return None
        elif check_password_hash(rows[0][0], password):
            # correct password
            return True
        else:
            return False

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
select password, id, email, firstname, lastname, address
from users
where email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, address):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, address)
VALUES(:email, :password, :firstname, :lastname, :address)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, 
                                  address=address)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None
    

    @staticmethod
    def update_profile(id, email, firstname, lastname, address):
        try:
            rows = app.db.execute("""
UPDATE Users
SET email = :email, firstname = :firstname, lastname = :lastname, address = :address
WHERE id = :id
RETURNING id
""",
                                  email=email,
                                  firstname=firstname, 
                                  lastname=lastname,
                                  address=address,
                                  id=id)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None
    

    @staticmethod
    def update_password(id, password):
        
        rows = app.db.execute("""
UPDATE Users
SET password = :password
WHERE id = :id
RETURNING id
""",
                                  password=generate_password_hash(password),
                                  id=id)
        id = rows[0][0]
        return User.get(id)
    

    @staticmethod
    def update_balance(id, deposit, withdraw):
        try:
            rows = app.db.execute("""
UPDATE Users
SET balance = balance + :diff
WHERE id = :id
RETURNING id
""",
                                  diff=(deposit-withdraw),
                                  id=id)
            id = rows[0][0]
            return User.get(id)
        
        except Exception as e:
            # it is possible that balance after deposit/withdraw is less than 0
            # it is checked by database system constraint
            print(e)
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    
    @staticmethod
    def get_balance(id):
        rows = app.db.execute("""
SELECT balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return rows[0][0]
