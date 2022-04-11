from unicodedata import category
from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
import pandas as pd

num_users = 100
num_products = 2000
num_purchases = 2500
num_orders = 500
num_sellers = 25
num_inventory = 6000
num_quantity = 100
num_carted_products = 200
num_user_carts = 40
num_prod_reviews = 1000
num_seller_reviews = 50

categories = [
    "Books",
    "Clothing",
    "Electronics",
    "Food",
    "Home",
    "Media",
    "Toys",
    "Sports",
]

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect="unix", quoting=csv.QUOTE_MINIMAL, escapechar='|')


def gen_users(num_users):
    with open("Users.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Users...", end=" ", flush=True)
        # add one test user for login
        email = "test@duke.edu"
        password = generate_password_hash("test")
        firstname = "test"
        lastname = "test"
        balance = 100
        address = "Durham NC"
        email_confirm = True  # without account activation
        writer.writerow(
            [0, email, password, firstname, lastname, balance, address, email_confirm]
        )
        print("Test user generated")

        for uid in range(1, num_users):
            if uid % 10 == 0:
                print(f"{uid}", end=" ", flush=True)
            profile = fake.profile()
            email = profile["mail"]
            plain_password = f"password_{uid}"
            password = generate_password_hash(plain_password)
            name_components = profile["name"].split(" ")
            firstname = name_components[0]
            lastname = name_components[-1]
            balance = random.randint(0, 100000)
            address = profile["address"]
            email_confirm = False  # requires account activation
            writer.writerow(
                [
                    uid,
                    email,
                    password,
                    firstname,
                    lastname,
                    balance,
                    address,
                    email_confirm
                ]
            )
        print(f"{num_users} users generated")

    return


def gen_sellers(num_sellers):

    """The first {num_sellers} users in Users will be sellers"""

    with open("Sellers.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Generating sellers ...")
        for sid in range(num_sellers):
            # whether or not wanna get notification when someone buys ur stuffs
            receive_notification = False
            writer.writerow([sid, receive_notification])
        print(f"{num_sellers} sellers generated")
        print(f"uid 0 to {num_sellers-1} are sellers")
    return


def gen_products(num_products):
    available_pids = []
    with open("Products.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Products...", end=" ", flush=True)
        for id in range(num_products):
            if id % 100 == 0:
                print(f"{id}", end=" ", flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            description = fake.sentence(nb_words=15)[:-1]
            available = fake.random_element(elements=("true", "false"))
            if available == "true":
                available_pids.append(id)
            category = fake.random_element(elements=categories)
            image_file = "https://source.unsplash.com/random/800x800/?img=1" + str(id)
            writer.writerow([id, name, description, available, category, image_file])
        print(f"{num_products} generated; {len(available_pids)} available")
    return available_pids


def gen_orders(num_orders):
    dict_oid_bid = {}
    with open("Orders.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Orders...", end=" ", flush=True)
        for id in range(num_orders):
            # id = fake.random_int(min=0, max=num_orders-1)
            bid = fake.random_int(min=0, max=num_users - 1)
            address = fake.profile()["address"]
            placed_datetime = fake.date_time()
            completed_status = fake.random_element(elements=("true", "false"))
            
            if completed_status == "true":
                completion_datetime = fake.date_time()
            else:
                completion_datetime = None

            dict_oid_bid[id] = bid

            writer.writerow(
                [
                    id,
                    bid,
                    address,
                    placed_datetime, 
                    completed_status,
                    completion_datetime
                ]
            )
    print(f"{num_orders} generated")

    return dict_oid_bid


def gen_purchases(
    num_orders, num_purchases, available_pids, dict_pid_sid, dict_oid_bid
):
    dict_oid_pid = {}
    dict_pid_bid = {}
    dict_sid_bid = {}

    oid_pid_sid = set()

    with open("Purchases.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Purchases...", end=" ", flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f"{id}", end=" ", flush=True)
            oid = fake.random_element(elements=dict_oid_bid.keys())
            pid = fake.random_element(elements=available_pids)
            # print(pid)
            sid = random.choice(dict_pid_sid.get(pid))

            # we should try a new pair if it is already exists
            while (oid, pid, sid) in oid_pid_sid:
                oid = fake.random_int(min=0, max=num_orders - 1)
                pid = fake.random_element(elements=available_pids)
                sid = random.choice(dict_pid_sid.get(pid))

            oid_pid_sid.add((oid, pid, sid))

            bid = dict_oid_bid.get(oid)
            price = f"{str(fake.random_int(max=1000))}.{fake.random_int(max=99):02}"
            quantity = fake.random_int(min=0, max=num_quantity)
            completed_status = fake.random_element(elements=("true", "false"))
            
            if completed_status == "true":
                completion_datetime = fake.date_time()
            else:
                completion_datetime = None

            if oid not in dict_oid_pid:
                dict_oid_pid[oid] = []
            dict_oid_pid[oid].append(pid)

            if pid not in dict_pid_bid:
                dict_pid_bid[pid] = []
            dict_pid_bid[pid].append(bid)

            if sid not in dict_sid_bid:
                dict_sid_bid[sid] = []
            dict_sid_bid[sid].append(bid)

            writer.writerow([oid, pid, sid, price, quantity, completed_status, completion_datetime])

    purchase_dicts = [dict_oid_pid, dict_pid_bid, dict_sid_bid]

    print(f"{num_purchases} generated")
    return purchase_dicts

""" def remove_quotes_purchases():
    with open('Purchases_quotes.csv', 'r') as input:
        with open('Purhcases.csv', 'a', newline='') as f:
            output = csv.writer(f, dialect='unix', delimiter=',', quoting=csv.QUOTE_NONE, escapechar='|')
            for row in input:
                output.writerow(row.replace('\"\"','').split(','))
    return

def remove_quotes_orders():
    with open('Orders_quotes.csv', 'r') as input:
        with open('Orders.csv', 'a', newline='') as f:
            output = csv.writer(f, dialect='unix', delimiter=',', quoting=csv.QUOTE_NONE, escapechar='|')
            for row in input:
                output.writerow(row.replace('\"\"','').split(','))
    return """


def gen_inventory(available_pids):
    dict_pid_sid = {}
    dict_pid_qty = {}
    with open("Inventory.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Inventory...", end=" ", flush=True)
        for pid in available_pids:
            sellers_this_item = random.randint(1, 9)
            for i in range(sellers_this_item):
                sid = fake.random_int(min=0, max=num_sellers - 1)
                while (pid in dict_pid_sid) and (sid in dict_pid_sid.get(pid)):
                    sid = fake.random_int(min=0, max=num_sellers - 1)
                if pid not in dict_pid_sid:
                    dict_pid_sid[pid] = []
                dict_pid_sid.get(pid).append(sid)
                price = f"{str(fake.random_int(max=1000))}.{fake.random_int(max=99):02}"
                quantity = fake.random_int(min=0, max=num_quantity)
                dict_pid_qty[pid] = quantity
                writer.writerow([pid, sid, price, quantity])
    print(f"{num_inventory} generated")
    inventory_dicts = [dict_pid_sid, dict_pid_qty]
    return inventory_dicts


def gen_cart(num_carted_products, num_user_carts, dict_pid_sid, available_pids):

    uid_pid_sid = set()

    with open("Cart.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Cart...", end=" ", flush=True)
        for id in range(num_carted_products):
            if id % 100 == 0:
                print(f"{id}", end=" ", flush=True)
            uid = fake.random_int(min=0, max=num_users - 1)
            pid = fake.random_element(elements=available_pids)
            sid = random.choice(dict_pid_sid.get(pid))

            while (uid, pid, sid) in uid_pid_sid:
                uid = fake.random_int(min=0, max=num_users - 1)
                pid = fake.random_element(elements=available_pids)
                sid = random.choice(dict_pid_sid.get(pid))

            uid_pid_sid.add((uid, pid, sid))

            price = f"{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}"
            quantity = fake.random_int(min=0, max=10)
            wishlist = fake.random_element(elements=("true", "false"))
            writer.writerow([uid, pid, sid, quantity, price, wishlist])
        print(f"{num_carted_products} generated")
    return


""" def gen_dict_pid_bid(dict_oid_bid, dict_oid_pid): 
    dict_pid_bid = {}
    for oid in dict_oid_pid:
        pid = dict_oid_pid.get(oid)
        bid = dict_oid_bid.get(oid)
        if pid not in dict_pid_bid:
            dict_pid_bid[pid] = []
        dict_pid_bid[pid].append(bid)
    return dict_pid_bid """


def gen_prod_reviews(num_prod_reviews, dict_pid_bid):

    pid_uid = set()

    with open("Reviews.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Product Reviews...", end=" ", flush=True)
        for i in range(num_prod_reviews):
            pid = fake.random_element(elements=dict_pid_bid.keys())
            bid = random.choice(dict_pid_bid.get(pid))

            while (pid, bid) in pid_uid:
                pid = fake.random_element(elements=dict_pid_bid.keys())
                bid = random.choice(dict_pid_bid.get(pid))

            pid_uid.add((pid, bid))

            display_name = fake.sentence(nb_words=2)[:-1]
            rating = random.randint(1, 5)
            title = fake.sentence(nb_words=4)[:-1]
            body = fake.sentence(nb_words=14)[:-1]
            submitted_ts = fake.date_time()
            writer.writerow([display_name, pid, bid, rating, title, body, submitted_ts])
    print("...Product Reviews done!")


def gen_reviews_sellers(num_seller_reviews, dict_sid_bid):

    sid_uid = set()

    with open("Reviews_sellers.csv", "w") as f:
        writer = get_csv_writer(f)
        print("Reviews...", end=" ", flush=True)
        for i in range(num_seller_reviews):
            sid = fake.random_element(elements=dict_sid_bid.keys())
            bid = random.choice(dict_sid_bid.get(sid))

            while (sid, bid) in sid_uid:
                sid = fake.random_element(elements=dict_sid_bid.keys())
                bid = random.choice(dict_sid_bid.get(sid))
            
            sid_uid.add((sid, bid))


            display_name = fake.sentence(nb_words=2)[:-1]
            rating = random.randint(1, 5)
            title = fake.sentence(nb_words=4)[:-1]
            body = fake.sentence(nb_words=14)[:-1]
            submitted_ts = fake.date_time()
            writer.writerow([display_name, sid, bid, rating, title, body, submitted_ts])
    print("...Sellers Reviews done!")


gen_users(num_users)
available_pids = gen_products(num_products)
# print(available_pids)
gen_sellers(num_sellers)
inventory_dicts = gen_inventory(available_pids)
dict_pid_sid = inventory_dicts[0]
dict_pid_qty = inventory_dicts[1]
dict_oid_bid = gen_orders(num_orders)
purchase_dicts = gen_purchases(
    num_orders, num_purchases, available_pids, dict_pid_sid, dict_oid_bid
)
dict_oid_pid = purchase_dicts[0]
dict_pid_bid = purchase_dicts[1]
dict_sid_bid = purchase_dicts[2]
#print(dict_pid_bid)
gen_cart(num_carted_products, num_user_carts, dict_pid_sid, available_pids)
gen_prod_reviews(num_prod_reviews, dict_pid_bid)
gen_reviews_sellers(num_seller_reviews, dict_sid_bid)
""" remove_quotes_orders()
remove_quotes_purchases() """
