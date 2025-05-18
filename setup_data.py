from database.db import DatabaseManager

db = DatabaseManager()

# Sample data
products = [
    ("Coca-Cola", True, "Mecca Cola"),
    ("Pepsi", True, "Qibla Cola"),
    ("Nestle", True, "Almarai"),
    ("Tapal Tea", False, None),
    ("BakeParlor", False, None),
    ("Starbucks", True, "Chai Shai"),
]

for name, is_israeli, alt in products:
    db.run_query("""
        INSERT OR REPLACE INTO products (name, is_israeli, alternative)
        VALUES (?, ?, ?)
    """, (name, is_israeli, alt))

print("✅ Product data inserted successfully!")
