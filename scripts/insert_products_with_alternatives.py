import sqlite3

DB_PATH = "database/baynah.db"

def add_product(cursor, barcode, product_name, brand, is_israeli, alt_product_id=None):
    cursor.execute("""
        INSERT OR IGNORE INTO products (barcode, product_name, brand, is_israeli, alt_product_id)
        VALUES (?, ?, ?, ?, ?)
    """, (barcode, product_name, brand, is_israeli, alt_product_id))

def get_product_by_name(cursor, name):
    cursor.execute("SELECT * FROM products WHERE LOWER(product_name) = ?", (name.lower(),))
    return cursor.fetchone()

def update_alt_product(cursor, product_name, alt_product_id):
    cursor.execute("""
        UPDATE products
        SET alt_product_id = ?
        WHERE LOWER(product_name) = ?
    """, (alt_product_id, product_name.lower()))

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    add_product(cursor, "9999999999999", "Next Cola", "Next Cola Inc.", False)
    conn.commit() 

    next_cola = get_product_by_name(cursor, "Next Cola")
    if not next_cola:
        print("❌ Failed to insert or fetch Next Cola.")
        return

    next_cola_id = next_cola[0]
    print(f"✅ Next Cola ID: {next_cola_id}")

    add_product(cursor, "0123456789012", "Pepsi", "PepsiCo", True, next_cola_id)
    conn.commit()

    pepsi = get_product_by_name(cursor, "Pepsi")
    if pepsi and pepsi[5] is None:
        update_alt_product(cursor, "Pepsi", next_cola_id)
        conn.commit()

    pepsi_updated = get_product_by_name(cursor, "Pepsi")
    print(f"✅ Pepsi alt_product_id = {pepsi_updated[5]}")

    conn.close()
    print("🎉 Products and alternative mapping complete.")

if __name__ == "__main__":
    main()
