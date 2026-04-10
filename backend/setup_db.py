import sqlite3
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

conn = sqlite3.connect('talk2data.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    salary REAL,
    hire_date TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price REAL,
    stock INTEGER
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity INTEGER,
    total_amount REAL,
    sale_date TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id)
)''')

cur.executemany('INSERT OR IGNORE INTO employees VALUES (?,?,?,?,?)', [
    (1, 'Rahul Sharma', 'Engineering', 75000, '2022-01-15'),
    (2, 'Priya Patel', 'Marketing', 62000, '2021-06-20'),
    (3, 'Amit Kumar', 'Engineering', 82000, '2020-03-10'),
    (4, 'Sneha Gupta', 'HR', 55000, '2023-02-28'),
    (5, 'Ravi Singh', 'Sales', 67000, '2021-11-05'),
    (6, 'Anjali Mehta', 'Engineering', 90000, '2019-08-12'),
    (7, 'Vikram Nair', 'Marketing', 71000, '2022-09-01'),
    (8, 'Kavya Reddy', 'Sales', 59000, '2023-05-15'),
])

cur.executemany('INSERT OR IGNORE INTO products VALUES (?,?,?,?,?)', [
    (1, 'Laptop', 'Electronics', 55000, 30),
    (2, 'Mouse', 'Electronics', 999, 150),
    (3, 'Keyboard', 'Electronics', 2500, 80),
    (4, 'Monitor', 'Electronics', 18000, 25),
    (5, 'Desk Chair', 'Furniture', 8500, 40),
    (6, 'Standing Desk', 'Furniture', 22000, 15),
    (7, 'Notebook', 'Stationery', 199, 500),
    (8, 'Pen Set', 'Stationery', 299, 300),
])

cur.executemany('INSERT OR IGNORE INTO sales VALUES (?,?,?,?,?)', [
    (1, 1, 5, 275000, '2024-01-10'),
    (2, 2, 20, 19980, '2024-01-12'),
    (3, 3, 10, 25000, '2024-01-15'),
    (4, 4, 3, 54000, '2024-02-01'),
    (5, 1, 2, 110000, '2024-02-10'),
    (6, 5, 8, 68000, '2024-02-14'),
    (7, 6, 3, 66000, '2024-03-01'),
    (8, 7, 100, 19900, '2024-03-10'),
])

conn.commit()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Database ready! Tables:", tables)

cur.execute("SELECT COUNT(*) FROM employees")
print("Employees:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM products")
print("Products:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM sales")
print("Sales:", cur.fetchone()[0])

conn.close()
