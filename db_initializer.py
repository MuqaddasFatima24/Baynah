import sqlite3

def create_db(db_path="database/baynah.db"):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = 1")  
    c = conn.cursor()

    # products table with alt_product_id foreign key
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT UNIQUE,
            product_name TEXT,
            brand TEXT,
            is_israeli BOOLEAN,
            alt_product_id INTEGER,
            FOREIGN KEY(alt_product_id) REFERENCES products(id)
        )
    """)

    # user table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT
        )
    """)
 # NGOs tables
    c.execute("""
        CREATE TABLE IF NOT EXISTS ngos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT,
            website TEXT
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
