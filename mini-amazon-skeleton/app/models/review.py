from flask import current_app as app
from flask_login import current_user

from .product import Product


class Review:
    def __init__(self, display_name, pid, uid, rating, title, body, submitted_ts):
        self.display_name = display_name
        self.pid = pid
        self.uid = uid
        self.rating = rating
        self.title = title
        self.body = body
        self.submitted_ts = submitted_ts

    @staticmethod
    def get_reviews_with_pid(pid):
        rows = app.db.execute('''
        SELECT display_name, pid, uid, rating, title, body, submitted_ts
        FROM Reviews 
        WHERE pid=:pid
        ORDER BY submitted_ts DESC
        ''',
        pid=pid)
        return [Review(*row) for row in rows]
    
    @staticmethod
    def get_reviews_with_pid(pid):
        rows = app.db.execute('''
SELECT R.display_name, R.pid, R.uid, R.rating, R.title, R.body, COALESCE(U.count, 0) AS cnt
FROM reviews R
LEFT JOIN (SELECT upvotes.userid, count(distinct upvotes.upvoteid) as count FROM upvotes
           WHERE upvotes.productid = :pid GROUP BY upvotes.userid) U
ON R.uid = U.userid
WHERE R.pid = :pid
ORDER BY cnt DESC, submitted_ts DESC
        ''',
        pid=pid)
        return rows

    @staticmethod
    def get_reviews_with_pid(pid):
        rows = app.db.execute('''
SELECT A.display_name, A.pid, A.uid, A.rating, A.title, A.body, A.cnt, A.submitted_ts, COALESCE(B.rcnt, 0) AS reviewcnt
FROM (SELECT R.display_name, R.pid, R.uid, R.rating, R.title, R.body, R.submitted_ts, COALESCE(U.count, 0) AS cnt
FROM reviews R
LEFT JOIN (SELECT upvotes.userid, count(distinct upvotes.upvoteid) as count FROM upvotes
           WHERE upvotes.productid = :pid GROUP BY upvotes.userid) U
ON R.uid = U.userid
WHERE R.pid = :pid) A
LEFT JOIN (SELECT reviews.uid, count(reviews.pid) AS rcnt
FROM reviews GROUP BY reviews.uid) B
ON A.uid = B.uid
ORDER BY cnt DESC, submitted_ts DESC
        ''',
        pid=pid)
        return rows

    @staticmethod
    def get_reviews_with_uid(uid):
        rows = app.db.execute('''
        SELECT display_name, pid, uid, rating, title, body, submitted_ts
        FROM Reviews 
        WHERE uid=:uid
        ORDER BY submitted_ts DESC
        ''',
        uid=uid)
        return [Review(*row) for row in rows]


    @staticmethod
    def avg_rating(pid):
        num = app.db.execute('''
        SELECT ROUND(AVG(rating),2)
        FROM Reviews
        WHERE pid=:pid
        ''',
        pid=pid)

        if num == None:
            return "No reviews for this product"
        else:
            return num[0][0]

    @staticmethod
    def count_reviews(pid):
        num = app.db.execute('''
        SELECT COUNT(rating)
        FROM Reviews
        WHERE pid=:pid
        ''',
        pid=pid)

        if num == None:
            return ""
        else:
            return num[0][0]
