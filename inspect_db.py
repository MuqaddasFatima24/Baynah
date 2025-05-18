import sqlite3

conn = sqlite3.connect("baynah.db")
cursor = conn.cursor()

def show_table(name):
    print(f"\n{name.upper()}:")
    for row in cursor.execute(f"SELECT * FROM {name}"):
        print(row)

for table in ['users', 'products', 'ngos']:
    try:
        show_table(table)
    except sqlite3.OperationalError as e:
        print(f"Error reading {table}: {e}")

conn.close()
