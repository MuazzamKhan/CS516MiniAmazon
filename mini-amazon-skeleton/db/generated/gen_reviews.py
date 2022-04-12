from unicodedata import category
import csv
import pandas as pd
from faker import Faker
import random 


Faker.seed(0)
fake = Faker()
num_reviews = 100
num_seller_reviews = 20

# get available uid/pid pairs 
# (gen reviews from users that bought the item)
order_fields = ['id', 'bid', 'address', 'placed_datetime', 'completed_status', 'completion_datetime']
orders = pd.read_csv('Orders.csv',names = order_fields)
purchases_fields = ['oid', 'pid', 'sid', 'price', 'quantity', 'completed_status', 'completion_datetime']
purchases = pd.read_csv('Purchases.csv', names = purchases_fields)

available_tuples = orders.merge(purchases, left_on = 'id', right_on = 'oid')[['bid', 'pid', 'sid', 'placed_datetime']]
available_tuples['placed_datetime'] = pd.to_datetime(available_tuples.placed_datetime)


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_reviews(num_reviews):
    id_pairs = available_tuples.sample(num_reviews, ignore_index = True)
    with open('Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for i in range(num_reviews):
            display_name = fake.sentence(nb_words=2)[:-1]
            pid = id_pairs.pid[i]
            uid = id_pairs.bid[i]
            rating = random.randint(1,5)
            title = fake.sentence(nb_words=4)[:-1]
            body = fake.sentence(nb_words=14)[:-1]
            submitted_ts = id_pairs.placed_datetime[i]
            writer.writerow([display_name, pid, uid, rating, title, body, submitted_ts])
    print('...Reviews done!')
    
def gen_reviews_sellers(num_reviews):
    id_pairs = available_tuples.sample(num_reviews, ignore_index = True)
    with open('Reviews_sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for i in range(num_reviews):
            display_name = fake.sentence(nb_words=2)[:-1]
            sid = id_pairs.sid[i]
            uid = id_pairs.bid[i]
            rating = random.randint(1,5)
            title = fake.sentence(nb_words=4)[:-1]
            body = fake.sentence(nb_words=14)[:-1]
            submitted_ts = id_pairs.placed_datetime[i]
            writer.writerow([display_name, sid, uid, rating, title, body, submitted_ts])
    print('...Reviews done!')
    

gen_reviews(100)
gen_reviews_sellers(20)