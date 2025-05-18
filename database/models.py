from .db import DatabaseManager

class User:
    def __init__(self, db):
        self.db = db

    def add_user(self, username, email, password):
        self.db.run_query(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

class Product:
    def __init__(self, db):
        self.db = db

    def add_product(self, barcode, product_name, brand, is_israeli, alt_product_id=None):
        self.db.run_query(
            """
            INSERT INTO products (barcode, product_name, brand, is_israeli, alt_product_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (barcode, product_name, brand, is_israeli, alt_product_id)
        )

    def get_product_by_name_or_barcode(self, search_term):
        query = """
        SELECT * FROM products
        WHERE barcode = ? OR LOWER(product_name) = LOWER(?) OR LOWER(brand) = LOWER(?)
        """
        result = self.db.cursor.execute(query, (search_term, search_term, search_term)).fetchone()
        return result

class NGO:
    def __init__(self, db):
        self.db = db

    def add_ngo(self, name, country, website):
        self.db.run_query(
            "INSERT INTO ngos (name, country, website) VALUES (?, ?, ?)",
            (name, country, website)
        )
