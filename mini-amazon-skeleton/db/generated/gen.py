from unicodedata import category
from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random 

num_users = 100
num_products = 2000
num_purchases = 2500
num_sellers = 15
num_inventory = 6000
num_carted_products = 200

categories = ['Books', 'Clothing', 'Electronics', 'Food', 'Home', 'Media', 'Toys', 'Sports']

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            balance = random.randint(0, 100000)
            address = profile['address']
            writer.writerow([uid, email, password, firstname, lastname, balance, address])
        print(f'{num_users} generated')
    return

def gen_sellers(num_sellers):
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for id in range(num_users):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            writer.writerow([id])
        print(f'{num_sellers} generated')
    return


def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            description = fake.sentence(nb_words=15)[:-1]
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            category = fake.random_element(elements=categories)
            image_file = 'https://picsum.photos/id/' + str(pid) + '/200/300'
            writer.writerow([pid, name, description, available, category, image_file])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

def gen_inventory(num_inventory):
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        for id in range(num_inventory):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            pid = fake.random_int(min=0, max=num_products-1)
            sid = fake.random_int(min=0, max=num_sellers-1)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            quantity = fake.random_int(min=0, max=100)
            writer.writerow([pid, sid, price, quantity])
        print(f'{num_inventory} generated')
    return


def gen_cart(num_carted_products):
    with open('Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        for id in range(num_carted_products):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_int(min=0, max=num_products-1)
            sid = fake.random_int(min=0, max=num_sellers-1)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            quantity = fake.random_int(min=0, max=10)
            wishlist = fake.random_element(elements=('true', 'false'))
            writer.writerow([uid, pid, sid, quantity, price, wishlist])
        print(f'{num_carted_products} generated')
    return

gen_users(num_users)
# available_pids = gen_products(num_products)
# gen_sellers(num_sellers)
# gen_purchases(num_purchases, available_pids)
# gen_inventory(num_inventory)
# gen_cart(num_carted_products)
