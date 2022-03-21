#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 23:37:23 2022

@author: jiwooky
"""

import sqlite3

def connect_reviewsdb():
    conn = sqlite3.connect('reviews.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS reviews")
    cur.execute(""""CREATE TABLE IF NOT EXISTS reviews
                (item_id TEXT, customer_id TEXT, review_score INT, reivew_title TEXT, reivew_body TEXT""")
    conn.commit()
    conn.close()

def insert_item(item_id, customer_id, catagory_id, review_date, review_score, review_title, review_body):
    conn = sqlite3.connect('reviews.db')
    cur = conn.cursor()
    cur.execute(""""CREATE TABLE IF NOT EXISTS reviews
                (item_id INT, customer_id INT, catagory_id INT, review_date INT,
                 review_score INT, reivew_title TEXT, reivew_body TEXT""")
    conn.commit()
    conn.close()

# vanilla review display feature: order by most recent similiar to the way amazon displays reviews
def get_all_reviews(item_id):
    conn = sqlite3.connect('reviews.db')
    cur = conn.cursor()
    cur.execute("SELECT review_date, review_score, review_title, review_body FROM reviews WHERE item_reviews = ? ORDER BY review_date DESC", (item_id))
    rows = cur.fetchall()
    conn.close()
    return rows

# super reviewer feature
def get_top_reviews(item_id):
    conn = sqlite3.connect('reviews.db')
    cur = conn.cursor()
    cur.execute(""""SELECT R.review_date, R.review_score, R.review_title, R.review_body FROM reviews AS R,
                (SELECT temp.customer_id, COUNT(*) as temp.review_cnt FROM reviews AS temp, GROUP BY temp.customer_id LIMIT 3) AS T
                WHERE R.item_reviews = ? AND R.customer_id = T.customer_id
                ORDER BY review_date DESC""", (item_id))
    rows = cur.fetchall()
    conn.close()
    return rows



