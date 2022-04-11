from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login
from datetime import datetime


class User(UserMixin):
    
    class Review:
        def __init__(self, title, body, rating, uid):
            self.title = title 
            self.body = body
            self.rating = rating
            self.uid = uid

    def __init__(self, id, email, firstname, lastname, address, is_seller, email_confirm=False, title=[], body=[], rating=[], uid=[]):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        
        self.is_seller = True if is_seller is not None else False
        self.email_confirm = False if not email_confirm else True
        self.reviews = []

        if self.is_seller:
            for idx, _ in enumerate(title):
                if _ is not None:
                    review = self.Review(title[idx], body[idx], rating[idx], uid[idx])
                    self.reviews.append(review)
        


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
    def get_email(id):
        rows = app.db.execute("""
select email
from users
where id = :id
""",
                              id=id)
        if not rows:  # email not found
            return None
        else:
            return rows[0][0]


    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
select password, id, email, firstname, lastname, address, FALSE as is_seller, email_confirm
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
    def confirm_email(email):
        
        rows = app.db.execute("""
UPDATE Users
SET email_confirm = true
WHERE email = :email
RETURNING id
""",
                                  email=email)
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
SELECT id, email, firstname, lastname, address, 
        CASE 
            WHEN id in (SELECT id FROM Sellers) THEN true ELSE false
        END AS is_seller,
       email_confirm, ARRAY_AGG(title), ARRAY_AGG(body), ARRAY_AGG(rating), ARRAY_AGG(uid)
FROM Users 
LEFT JOIN Reviews_sellers ON id = sid
WHERE id = :id
GROUP BY id, email, firstname, lastname, address, sid, email_confirm
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

    @staticmethod
    def leave_review(display_name, uid, pid, rating, title, body):
            rows = app.db.execute("""
                    INSERT INTO Reviews(display_name, uid, pid, rating, title, body, submitted_ts) 
                    VALUES(:display_name, :uid, :pid, :rating, :title, :body, :submitted_ts)
                    ON CONFLICT (pid, uid) DO UPDATE
                    SET display_name = :display_name, rating = :rating, title = :title, body = :body, submitted_ts = :submitted_ts
                    RETURNING uid
                """,
                        display_name = display_name,
                        uid=uid,
                        pid=pid, 
                        rating=rating,
                        title=title,
                        body=body,
                        submitted_ts=datetime.now())

                #id = rows[0][0]

            return id if rows else None

