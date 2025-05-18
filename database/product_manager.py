import os
import sqlite3

class ProductManager:
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, "baynah.db")

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables() 

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            barcode TEXT UNIQUE,
            product_name TEXT,
            brand TEXT,
            is_israeli BOOLEAN,
            alt_product_id INTEGER,
            FOREIGN KEY(alt_product_id) REFERENCES products(id)
        )
        """)
        self.conn.commit()

    def search_product(self, query):
        query = f"%{query.lower()}%"
        self.cursor.execute("""
        SELECT * FROM products 
        WHERE LOWER(barcode) LIKE ? OR LOWER(product_name) LIKE ? OR LOWER(brand) LIKE ?
        LIMIT 1
        """, (query, query, query))
        return self.cursor.fetchone()

    def get_product_by_id(self, pid):
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (pid,))
        return self.cursor.fetchone()

    def add_product(self, barcode, product_name, brand, is_israeli, alt_id=None):
        self.cursor.execute("""
        INSERT OR IGNORE INTO products (barcode, product_name, brand, is_israeli, alt_product_id)
        VALUES (?, ?, ?, ?, ?)
        """, (barcode, product_name, brand, is_israeli, alt_id))
        self.conn.commit()
