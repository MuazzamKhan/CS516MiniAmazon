from unicodedata import category
from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random 

num_users = 100
num_products = 2000
num_purchases = 2500
num_orders = 500
num_sellers = 25
num_inventory = 6000
num_quantity = 100
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
        
        # add one test user for login
        email = 'test@duke.edu'
        password = generate_password_hash("test")
        firstname = 'test'
        lastname = 'test'
        balance = 100
        address = 'Durham NC'
        email_confirm = True # without account activation 
        writer.writerow([0, email, password, firstname, lastname, balance, address, email_confirm])
        print("Test user generated")

        for uid in range(1, num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'password_{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            balance = random.randint(0, 100000)
            address = profile['address']
            email_confirm = False # requires account activation 
            writer.writerow([uid, email, password, firstname, lastname, balance, address, email_confirm])
        print(f'{num_users} users generated')

    return

def gen_sellers(num_sellers):
    
    """ The first {num_sellers} users in Users will be sellers """

    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print("Generating sellers ...")
        for sid in range(num_sellers):
            # whether or not wanna get notification when someone buys ur stuffs
            receive_notification = False
            writer.writerow([sid, receive_notification])
        print(f'{num_sellers} sellers generated')
        print(f'uid 0 to {num_sellers-1} are sellers')
    return


def gen_products(num_products):
    with open('Products.csv', 'w') as f:
        available_pids = []
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for id in range(num_products):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            description = fake.sentence(nb_words=15)[:-1]
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(id)
            category = fake.random_element(elements=categories)
            image_file = 'https://source.unsplash.com/random/800x800/?img=1' + str(id)
            writer.writerow([id, name, description, available, category, image_file])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            oid = fake.random_int(min=0, max=num_orders-1)
            pid = fake.random_element(elements=available_pids)
            sid = fake.random_int(min=0, max=num_sellers-1)
            price = f'{str(fake.random_int(max=1000))}.{fake.random_int(max=99):02}'
            quantity = fake.random_int(min=0, max=num_quantity)
            completed_status = fake.random_element(elements=('true', 'false'))
            completion_datetime = fake.date_time()
            writer.writerow([oid, pid, sid, price, quantity, completed_status, completion_datetime])
        print(f'{num_purchases} generated')
    return

def gen_orders(num_orders):
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for id in range(num_orders):
            id = fake.random_int(min=0, max=num_orders-1)
            bid = fake.random_int(min=0, max=num_users-1)
            address = fake.profile()['address']
            placed_datetime = fake.date_time()
            completed_status = fake.random_element(elements=('true', 'false'))
            completion_datetime = fake.date_time()
            writer.writerow([id, bid, address, placed_datetime, completed_status, completion_datetime])
        print(f'{num_orders} generated')
    return

def gen_inventory(num_inventory):
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        for id in range(num_inventory):
            pid = fake.random_int(min=0, max=num_products-1)
            sid = fake.random_int(min=0, max=num_sellers-1)
            price = f'{str(fake.random_int(max=1000))}.{fake.random_int(max=99):02}'
            quantity = fake.random_int(min=0, max=num_quantity)
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
available_pids = gen_products(num_products)
gen_sellers(num_sellers)
gen_purchases(num_purchases, available_pids)
gen_inventory(num_inventory)
