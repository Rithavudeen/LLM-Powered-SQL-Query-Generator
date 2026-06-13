import sqlite3
import pandas as pd
import os

DB_PATH = "data/demo.db"

def init_database():
    """Initialize SQLite database with sample data."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            city TEXT,
            state TEXT,
            phone TEXT,
            created_at DATE DEFAULT CURRENT_DATE
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock_quantity INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date DATE DEFAULT CURRENT_DATE,
            total_amount REAL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );

        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            payment_date DATE DEFAULT CURRENT_DATE,
            amount REAL,
            method TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        );
    """)

    # Insert sample data only if tables are empty
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        customers = [
            ("Aarav Sharma", "aarav@email.com", "Mumbai", "Maharashtra", "9876543210"),
            ("Priya Patel", "priya@email.com", "Bangalore", "Karnataka", "9876543211"),
            ("Rohan Gupta", "rohan@email.com", "Delhi", "Delhi", "9876543212"),
            ("Sneha Reddy", "sneha@email.com", "Hyderabad", "Telangana", "9876543213"),
            ("Karan Mehta", "karan@email.com", "Chennai", "Tamil Nadu", "9876543214"),
            ("Ananya Singh", "ananya@email.com", "Pune", "Maharashtra", "9876543215"),
            ("Vikram Joshi", "vikram@email.com", "Kolkata", "West Bengal", "9876543216"),
            ("Divya Nair", "divya@email.com", "Mumbai", "Maharashtra", "9876543217"),
            ("Arjun Kumar", "arjun@email.com", "Bangalore", "Karnataka", "9876543218"),
            ("Meera Iyer", "meera@email.com", "Chennai", "Tamil Nadu", "9876543219"),
        ]
        cursor.executemany(
            "INSERT INTO customers (name, email, city, state, phone) VALUES (?, ?, ?, ?, ?)",
            customers
        )

        products = [
            ("Laptop Pro 15", "Electronics", 75000.00, 50),
            ("Wireless Mouse", "Electronics", 1500.00, 200),
            ("Office Chair", "Furniture", 12000.00, 30),
            ("Standing Desk", "Furniture", 25000.00, 15),
            ("USB Hub", "Electronics", 2500.00, 100),
            ("Notebook Set", "Stationery", 500.00, 500),
            ("Mechanical Keyboard", "Electronics", 5000.00, 75),
            ("Monitor 27 inch", "Electronics", 22000.00, 40),
            ("Webcam HD", "Electronics", 3500.00, 60),
            ("Desk Lamp", "Furniture", 1800.00, 120),
        ]
        cursor.executemany(
            "INSERT INTO products (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)",
            products
        )

        orders = [
            (1, "2024-01-15", 76500.00, "delivered"),
            (2, "2024-01-20", 13500.00, "delivered"),
            (3, "2024-02-05", 27500.00, "delivered"),
            (4, "2024-02-10", 4000.00, "shipped"),
            (5, "2024-02-28", 22000.00, "delivered"),
            (6, "2024-03-01", 75000.00, "delivered"),
            (7, "2024-03-15", 8500.00, "pending"),
            (1, "2024-03-20", 5000.00, "delivered"),
            (2, "2024-04-01", 25500.00, "delivered"),
            (3, "2024-04-10", 3500.00, "shipped"),
        ]
        cursor.executemany(
            "INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)",
            orders
        )

        order_items = [
            (1, 1, 1, 75000.00), (1, 2, 1, 1500.00),
            (2, 3, 1, 12000.00), (2, 6, 1, 1500.00),
            (3, 4, 1, 25000.00), (3, 6, 5, 2500.00),
            (4, 5, 2, 2000.00),
            (5, 8, 1, 22000.00),
            (6, 1, 1, 75000.00),
            (7, 3, 1, 5000.00), (7, 10, 1, 1800.00), (7, 9, 1, 1700.00),
        ]
        cursor.executemany(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
            order_items
        )

        payments = [
            (1, "2024-01-15", 76500.00, "UPI"),
            (2, "2024-01-20", 13500.00, "Credit Card"),
            (3, "2024-02-05", 27500.00, "Net Banking"),
            (5, "2024-02-28", 22000.00, "Debit Card"),
            (6, "2024-03-01", 75000.00, "UPI"),
            (8, "2024-03-20", 5000.00, "Credit Card"),
            (9, "2024-04-01", 25500.00, "Net Banking"),
        ]
        cursor.executemany(
            "INSERT INTO payments (order_id, payment_date, amount, method) VALUES (?, ?, ?, ?)",
            payments
        )

    conn.commit()
    conn.close()


def execute_query(sql: str) -> pd.DataFrame:
    """
    Execute SQL query on demo database.

    Args:
        sql: SQL query string

    Returns:
        DataFrame with query results
    """
    init_database()
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
        return df
    except Exception as e:
        raise Exception(f"Query execution failed: {str(e)}")
    finally:
        conn.close()


def get_schema_info() -> str:
    """Return schema info as formatted string."""
    return """-- customers
customer_id, name, email, city, state, phone, created_at

-- products
product_id, name, category, price, stock_quantity

-- orders
order_id, customer_id, order_date, total_amount, status

-- order_items
item_id, order_id, product_id, quantity, unit_price

-- payments
payment_id, order_id, payment_date, amount, method"""
