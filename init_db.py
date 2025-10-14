import sqlite3
from datetime import datetime, timedelta
import random
import os
from werkzeug.security import generate_password_hash
import names
from faker import Faker

def init_database():
    os.makedirs('database', exist_ok=True)
    
    conn = sqlite3.connect('database/picknpay.db')
    c = conn.cursor()
    
    # Drop existing tables
    c.execute('DROP TABLE IF EXISTS transaction_items')
    c.execute('DROP TABLE IF EXISTS transactions')
    c.execute('DROP TABLE IF EXISTS customers')
    c.execute('DROP TABLE IF EXISTS products')
    
    # Create tables
    c.execute('''CREATE TABLE products (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 category TEXT NOT NULL,
                 price REAL NOT NULL,
                 supplier TEXT,
                 barcode TEXT UNIQUE)''')
    
    c.execute('''CREATE TABLE customers (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 gender TEXT,
                 age_group TEXT,
                 location TEXT,
                 loyalty_tier TEXT,
                 email TEXT,
                 join_date TEXT)''')
    
    c.execute('''CREATE TABLE transactions (
                 id INTEGER PRIMARY KEY,
                 customer_id INTEGER NOT NULL,
                 timestamp TEXT NOT NULL,
                 total_amount REAL NOT NULL,
                 payment_method TEXT,
                 store_id INTEGER,
                 FOREIGN KEY(customer_id) REFERENCES customers(id))''')
    
    c.execute('''CREATE TABLE transaction_items (
                 id INTEGER PRIMARY KEY,
                 transaction_id INTEGER NOT NULL,
                 product_id INTEGER NOT NULL,
                 quantity INTEGER NOT NULL,
                 unit_price REAL NOT NULL,
                 discount REAL DEFAULT 0,
                 FOREIGN KEY(transaction_id) REFERENCES transactions(id),
                 FOREIGN KEY(product_id) REFERENCES products(id))''')
    
    # Generate sample data
    fake = Faker()
    
    # Products
    products = []
    categories = {
        'Bakery': ['Bread', 'Croissant', 'Muffins'],
        'Dairy': ['Milk', 'Cheese', 'Yogurt'],
        'Beverages': ['Coke', 'Juice', 'Water']
    }
    
    product_id = 1
    for category, items in categories.items():
        for item in items:
            price = round(random.uniform(1.0, 10.0), 2)
            products.append((product_id, f'{item}', category, price, fake.company(), fake.ean13()))
            product_id += 1
    
    c.executemany('INSERT INTO products VALUES (?,?,?,?,?,?)', products)
    
    # Customers
    customers = []
    for i in range(1, 101):
        gender = random.choice(['Male', 'Female'])
        name = names.get_full_name(gender=gender.lower())
        customers.append((
            i, name, gender, random.choice(['18-25', '26-35', '36-45']),
            random.choice(['Johannesburg', 'Cape Town']),
            random.choice(['Bronze', 'Silver', 'Gold']),
            fake.email(), fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
        ))
    
    c.executemany('INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)', customers)
    
    # Transactions
    transaction_id = 1
    for day in range(60):  # Last 60 days
        current_date = datetime.now() - timedelta(days=60 - day - 1)
        daily_transactions = random.randint(50, 100)
        
        for _ in range(daily_transactions):
            customer_id = random.randint(1, 100)
            timestamp = current_date.replace(
                hour=random.randint(8, 20),
                minute=random.randint(0, 59)
            ).strftime('%Y-%m-%d %H:%M:%S')
            
            c.execute('INSERT INTO transactions VALUES (?,?,?,?,?,?)',
                     (transaction_id, customer_id, timestamp, 0, 
                      random.choice(['Cash', 'Card']), 1))
            
            # Transaction items
            total = 0
            items_count = random.randint(1, 5)
            selected_products = random.sample(products, min(items_count, len(products)))
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                unit_price = product[3]
                item_total = quantity * unit_price
                total += item_total
                
                c.execute('INSERT INTO transaction_items VALUES (?,?,?,?,?,?)',
                         (None, transaction_id, product[0], quantity, unit_price, 0))
            
            c.execute('UPDATE transactions SET total_amount=? WHERE id=?', 
                     (round(total, 2), transaction_id))
            transaction_id += 1
    
    conn.commit()
    conn.close()
    print("Sample database created successfully!")

if __name__ == '__main__':
    init_database()