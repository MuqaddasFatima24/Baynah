import os
import sqlite3

class DatabaseManager:
    def __init__(self):
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