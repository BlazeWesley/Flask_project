import sqlite3
import random
from datetime import datetime, timedelta
import os

# Remove existing database file if it exists
if os.path.exists('picknpay_zimbabwe.db'):
    os.remove('picknpay_zimbabwe.db')

# Connect to SQLite database
conn = sqlite3.connect('picknpay_zimbabwe.db')
cursor = conn.cursor()

print("🛒 Creating Pick n Pay Zimbabwe Database (July-Sept 2025)...")

# Create Tables
cursor.executescript('''
CREATE TABLE Customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT,
    location TEXT,
    loyalty_tier TEXT
);

CREATE TABLE Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    timestamp TEXT NOT NULL,
    total_amount REAL NOT NULL,
    payment_method TEXT NOT NULL,
    store_id INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(id)
);

CREATE TABLE Transaction_Items (
    transaction_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    PRIMARY KEY (transaction_id, product_id),
    FOREIGN KEY (transaction_id) REFERENCES Transactions(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);
''')

# Zimbabwean Names Data
zimbabwean_names = [
    ('Tendai Moyo', 'Male', 'Harare'), ('Rumbidzai Chiweshe', 'Female', 'Harare'),
    ('Takudzwa Ndlovu', 'Male', 'Bulawayo'), ('Shamiso Marufu', 'Female', 'Mutare'),
    ('Tinashe Sibanda', 'Male', 'Gweru'), ('Nyasha Machona', 'Female', 'Harare'),
    ('Farai Banda', 'Male', 'Bulawayo'), ('Rutendo Gumbo', 'Female', 'Masvingo'),
    ('Kudakwashe Hove', 'Male', 'Harare'), ('Chengetai Mapfumo', 'Female', 'Chitungwiza'),
    ('Blessing Mugabe', 'Male', 'Harare'), ('Precious Nkomo', 'Female', 'Bulawayo'),
    ('Tawanda Chirinda', 'Male', 'Kadoma'), ('Memory Dube', 'Female', 'Gweru'),
    ('Innocent Zulu', 'Male', 'Harare'), ('Sibongile Ncube', 'Female', 'Bulawayo'),
    ('Justice Maphosa', 'Male', 'Harare'), ('Fadzai Tshuma', 'Female', 'Victoria Falls'),
    ('Munyaradzi Chidziva', 'Male', 'Marondera'), ('Vongai Makoni', 'Female', 'Chegutu'),
    ('Tongai Chigumba', 'Male', 'Harare'), ('Yolanda Muzenda', 'Female', 'Bulawayo'),
    ('Godfrey Chidhakwa', 'Male', 'Mutare'), ('Beatrice Zhou', 'Female', 'Gweru'),
    ('Edmore Katsande', 'Male', 'Kwekwe'), ('Chiedza Mupfumi', 'Female', 'Harare'),
    ('Wellington Masakadza', 'Male', 'Bulawayo'), ('Patience Nyathi', 'Female', 'Masvingo'),
    ('Simbarashe Maruma', 'Male', 'Harare'), ('Ruvimbo Tshuma', 'Female', 'Chitungwiza'),
    ('Tafadzwa Machingauta', 'Male', 'Bindura'), ('Anesu Gumbo', 'Female', 'Norton'),
    ('Blessing Chinemhuka', 'Male', 'Harare'), ('Rudo Moyo', 'Female', 'Bulawayo'),
    ('Tawanda Muti', 'Male', 'Gweru'), ('Makanaka Sithole', 'Female', 'Mutare')
]

loyalty_tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']

# Insert Customers
for name, gender, location in zimbabwean_names:
    loyalty_tier = random.choice(loyalty_tiers)
    cursor.execute(
        "INSERT INTO Customers (name, gender, location, loyalty_tier) VALUES (?, ?, ?, ?)",
        (name, gender, location, loyalty_tier)
    )

# Pick n Pay Zimbabwe Products (updated with USD prices - approximately ZAR prices divided by 18.5)
products = [
    # Bakery (USD prices)
    ('Brown Bread 700g', 'Bakery', 0.68), ('White Bread 700g', 'Bakery', 0.62),
    ('Croissants 4pk', 'Bakery', 2.03), ('Rusks 250g', 'Bakery', 2.43),
    ('Buns 6pk', 'Bakery', 1.35), ('Cake Slice', 'Bakery', 0.97),
    
    # Dairy (USD prices)
    ('Lacto 500ml', 'Dairy', 1.05), ('Anchor Milk 1L', 'Dairy', 1.49),
    ('Cheddar Cheese 250g', 'Dairy', 2.84), ('Yoghurt 500ml', 'Dairy', 1.32),
    ('Butter 250g', 'Dairy', 2.08), ('Maas 500ml', 'Dairy', 0.89),
    
    # Meat & Poultry (USD prices)
    ('Chicken Breast 1kg', 'Meat', 5.14), ('Beef Steak 500g', 'Meat', 7.16),
    ('Boerewors 500g', 'Meat', 3.86), ('Pork Chops 500g', 'Meat', 4.19),
    ('Fish Fillets 500g', 'Meat', 4.46), ('Mince Meat 500g', 'Meat', 3.51),
    
    # Groceries (USD prices)
    ('Sugar 2kg', 'Groceries', 1.86), ('Cooking Oil 750ml', 'Groceries', 2.62),
    ('Mealie Meal 10kg', 'Groceries', 5.00), ('Rice 2kg', 'Groceries', 3.05),
    ('Baked Beans 410g', 'Groceries', 1.05), ('Flour 2kg', 'Groceries', 2.19),
    ('Tea Bags 100pk', 'Groceries', 2.03), ('Coffee 250g', 'Groceries', 3.51),
    
    # Produce (USD prices)
    ('Tomatoes 1kg', 'Produce', 1.54), ('Onions 1kg', 'Produce', 1.05),
    ('Potatoes 2kg', 'Produce', 1.92), ('Bananas 1kg', 'Produce', 1.22),
    ('Apples 1kg', 'Produce', 2.68), ('Oranges 1kg', 'Produce', 1.76),
    ('Carrots 1kg', 'Produce', 1.16), ('Cabbage each', 'Produce', 0.95),
    ('Spinach Bunch', 'Produce', 0.68), ('Green Beans 500g', 'Produce', 1.49),
    
    # Beverages (USD prices)
    ('Coca Cola 2L', 'Beverages', 1.32), ('Sprite 2L', 'Beverages', 1.32),
    ('Maheu 500ml', 'Beverages', 0.62), ('Still Water 1.5L', 'Beverages', 0.73),
    ('Orange Juice 1L', 'Beverages', 1.76), ('Apple Juice 1L', 'Beverages', 1.86),
    
    # Personal Care (USD prices)
    ('Colgate Toothpaste', 'Personal Care', 2.08), ('Protex Soap', 'Personal Care', 0.73),
    ('Surf Washing Powder', 'Personal Care', 2.78), ('Vaseline 100ml', 'Personal Care', 1.65),
    ('Shampoo 400ml', 'Personal Care', 2.57), ('Deodorant 150ml', 'Personal Care', 2.14),
    
    # Snacks (USD prices)
    ('Lays Chips 100g', 'Snacks', 1.05), ('Biscuits 200g', 'Snacks', 1.32),
    ('Chocolate Bar', 'Snacks', 0.89), ('Peanuts 200g', 'Snacks', 1.22),
    ('Popcorn 200g', 'Snacks', 1.00), ('Crisps 150g', 'Snacks', 1.16),
    
    # Frozen Foods (USD prices)
    ('Ice Cream 2L', 'Frozen', 4.84), ('Frozen Vegetables 500g', 'Frozen', 1.76),
    ('Frozen Chicken Pieces 1kg', 'Frozen', 4.24), ('Frozen Fish Fingers 500g', 'Frozen', 3.49)
]

# Insert Products
for product in products:
    cursor.execute(
        "INSERT INTO Products (name, category, price) VALUES (?, ?, ?)",
        product
    )

# Generate 3 months of transactions (July - September 2025)
print("📊 Generating 3 months of transaction data (July-Sept 2025)...")

payment_methods = ['Ecocash', 'Cash', 'Credit Card', 'Debit Card']
stores = [1, 2, 3]  # Store IDs

# Generate dates for 3 months (July 1 - September 30, 2025)
start_date = datetime(2025, 7, 1)
end_date = datetime(2025, 9, 30)
current_date = start_date

transaction_id = 1
seasonal_patterns = {
    7: {'name': 'July', 'factor': 1.0},  # Normal month
    8: {'name': 'August', 'factor': 1.2},  # Higher sales - Heroes Day, Women's Day
    9: {'name': 'September', 'factor': 1.3}  # Highest - Spring, end of winter
}

while current_date <= end_date:
    month_factor = seasonal_patterns[current_date.month]['factor']
    
    # More transactions on weekends and paydays (15th and 30th/31st)
    day_of_week = current_date.weekday()
    is_weekend = day_of_week >= 5
    is_payday = current_date.day in [15, 30, 31]
    
    # Special days with higher traffic
    is_heroes_day = current_date.month == 8 and current_date.day in [11, 12]  # Heroes Day weekend
    is_spring_start = current_date.month == 9 and current_date.day in [1, 2]  # Spring beginning
    
    if is_heroes_day or is_spring_start:
        base_transactions = random.randint(25, 35)
    elif is_weekend or is_payday:
        base_transactions = random.randint(15, 25)
    else:
        base_transactions = random.randint(8, 15)
    
    # Apply monthly seasonal factor
    daily_transactions = int(base_transactions * month_factor)
    
    for _ in range(daily_transactions):
        # Generate random time between 7 AM and 9 PM
        hour = random.randint(7, 21)
        minute = random.randint(0, 59)
        timestamp = current_date.replace(hour=hour, minute=minute, second=0)
        
        customer_id = random.randint(1, len(zimbabwean_names))
        payment_method = random.choice(payment_methods)
        store_id = random.choice(stores)
        
        # Insert transaction
        cursor.execute(
            "INSERT INTO Transactions (customer_id, timestamp, total_amount, payment_method, store_id) VALUES (?, ?, ?, ?, ?)",
            (customer_id, timestamp.strftime('%Y-%m-%d %H:%M:%S'), 0, payment_method, store_id)
        )
        
        # Add transaction items with seasonal variations
        num_items = random.randint(1, 8)
        transaction_total = 0
        
        # Seasonal product preferences
        seasonal_products = {
            7: ['Coffee', 'Tea Bags', 'Butter', 'Bread', 'Soup'],  # Winter items
            8: ['Chicken', 'Meat', 'Maheu', 'Snacks', 'Beverages'],  # Holiday cooking
            9: ['Fruits', 'Vegetables', 'Juice', 'Ice Cream', 'Spinach']  # Spring fresh items
        }
        
        preferred_categories = seasonal_products[current_date.month]
        
        # Use a set to track used product IDs for this transaction to avoid duplicates
        used_product_ids = set()
        
        for _ in range(num_items):
            # Bias towards seasonal products
            if random.random() < 0.3:  # 30% chance to pick seasonal product
                seasonal_product_ids = [i+1 for i, p in enumerate(products) 
                                     if any(cat in p[0] for cat in preferred_categories)]
                available_seasonal = [pid for pid in seasonal_product_ids if pid not in used_product_ids]
                if available_seasonal:
                    product_id = random.choice(available_seasonal)
                else:
                    # If no seasonal products available, pick any available product
                    available_products = [pid for pid in range(1, len(products)+1) if pid not in used_product_ids]
                    if available_products:
                        product_id = random.choice(available_products)
                    else:
                        break  # No more unique products available
            else:
                available_products = [pid for pid in range(1, len(products)+1) if pid not in used_product_ids]
                if available_products:
                    product_id = random.choice(available_products)
                else:
                    break  # No more unique products available
            
            used_product_ids.add(product_id)
            
            quantity = random.randint(1, 3)
            unit_price = products[product_id-1][2]  # Get price from products list
            
            # Occasionally apply promotions (more in September for spring cleaning)
            promo_chance = 0.15 if current_date.month == 9 else 0.1
            if random.random() < promo_chance:
                unit_price *= random.uniform(0.7, 0.85)  # 15-30% discount
            
            cursor.execute(
                "INSERT INTO Transaction_Items (transaction_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (transaction_id, product_id, quantity, round(unit_price, 2))
            )
            
            transaction_total += quantity * unit_price
        
        # Update transaction total
        cursor.execute(
            "UPDATE Transactions SET total_amount = ? WHERE id = ?",
            (round(transaction_total, 2), transaction_id)
        )
        
        transaction_id += 1
    
    # Progress indicator
    if current_date.day == 1:
        month_name = seasonal_patterns[current_date.month]['name']
        print(f"   Generating {month_name} 2025 data...")
    
    current_date += timedelta(days=1)

# Create indexes for better performance
cursor.executescript('''
CREATE INDEX idx_transactions_customer_id ON Transactions(customer_id);
CREATE INDEX idx_transactions_timestamp ON Transactions(timestamp);
CREATE INDEX idx_transactions_store_id ON Transactions(store_id);
CREATE INDEX idx_products_category ON Products(category);
CREATE INDEX idx_transaction_items_transaction_id ON Transaction_Items(transaction_id);
CREATE INDEX idx_transaction_items_product_id ON Transaction_Items(product_id);
''')

# Create useful views
cursor.executescript('''
CREATE VIEW Customer_Purchase_Summary AS
SELECT 
    c.id AS customer_id,
    c.name,
    c.location,
    c.loyalty_tier,
    COUNT(t.id) AS total_transactions,
    SUM(t.total_amount) AS total_spent,
    AVG(t.total_amount) AS avg_transaction_value,
    MAX(t.timestamp) AS last_purchase_date
FROM Customers c
LEFT JOIN Transactions t ON c.id = t.customer_id
GROUP BY c.id, c.name, c.location, c.loyalty_tier;

CREATE VIEW Product_Sales_Performance AS
SELECT 
    p.id AS product_id,
    p.name,
    p.category,
    SUM(ti.quantity) AS total_quantity_sold,
    SUM(ti.quantity * ti.unit_price) AS total_revenue,
    COUNT(DISTINCT ti.transaction_id) AS transaction_count,
    AVG(ti.quantity) AS avg_quantity_per_transaction
FROM Products p
JOIN Transaction_Items ti ON p.id = ti.product_id
GROUP BY p.id, p.name, p.category;

CREATE VIEW Monthly_Sales_Analysis AS
SELECT 
    strftime('%Y-%m', timestamp) as month,
    store_id,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM Transactions
GROUP BY strftime('%Y-%m', timestamp), store_id;

CREATE VIEW Seasonal_Product_Performance AS
SELECT 
    p.category,
    strftime('%Y-%m', t.timestamp) as month,
    SUM(ti.quantity) as total_quantity,
    SUM(ti.quantity * ti.unit_price) as total_revenue
FROM Products p
JOIN Transaction_Items ti ON p.id = ti.product_id
JOIN Transactions t ON ti.transaction_id = t.id
GROUP BY p.category, strftime('%Y-%m', t.timestamp)
ORDER BY month, total_revenue DESC;
''')

# Commit changes and close connection
conn.commit()

# Print summary
print("\n✅ Database Created Successfully!")
print("📁 File: picknpay_zimbabwe.db")

# Display statistics
cursor.execute("SELECT COUNT(*) FROM Customers")
print(f"👥 Customers: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM Products")
print(f"🛍️ Products: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM Transactions")
transactions_count = cursor.fetchone()[0]
print(f"🧾 Transactions: {transactions_count}")

cursor.execute("SELECT COUNT(*) FROM Transaction_Items")
transaction_items_count = cursor.fetchone()[0]
print(f"📦 Transaction Items: {transaction_items_count}")

cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM Transactions")
min_date, max_date = cursor.fetchone()
print(f"📅 Date Range: {min_date} to {max_date}")

cursor.execute("SELECT SUM(total_amount) FROM Transactions")
total_revenue = cursor.fetchone()[0]
print(f"💰 Total Revenue: ${total_revenue:,.2f} USD")  # Changed to USD

# Monthly breakdown
cursor.execute('''
SELECT strftime('%Y-%m', timestamp) as month, 
       COUNT(*) as transactions,
       SUM(total_amount) as revenue,
       AVG(total_amount) as avg_transaction
FROM Transactions 
GROUP BY strftime('%Y-%m', timestamp)
ORDER BY month
''')
print("\n📈 Monthly Breakdown (July-Sept 2025):")
for month, transactions, revenue, avg_trans in cursor.fetchall():
    print(f"   {month}: {transactions:>3} transactions, ${revenue:>8,.2f} revenue, ${avg_trans:>5.2f} avg")

# Top selling categories by month
cursor.execute('''
SELECT month, category, total_revenue 
FROM Seasonal_Product_Performance 
WHERE month IN ('2025-07', '2025-08', '2025-09')
ORDER BY month, total_revenue DESC
LIMIT 15
''')
print("\n🏆 Top Categories by Month:")
current_month = None
for month, category, revenue in cursor.fetchall():
    if month != current_month:
        print(f"   {month}:")
        current_month = month
    print(f"     - {category}: ${revenue:,.2f}")

conn.close()

print(f"\n🎯 Database is ready for ShopTrend Analytics!")
print("💡 You can now use this .db file in your application.")
print("📊 Features: Seasonal patterns, realistic Zimbabwean data, 3 months of transactions")
print("💰 All prices and revenue in USD")