from database.db import DatabaseManager
from database.models import User, Product, NGO

db = DatabaseManager()

user_manager = User(db)
product_manager = Product(db)
ngo_manager = NGO(db)

# sample data
user_manager.add_user("john_doe", "john@example.com", "securepassword123")
product_manager.add_product("Sabra Hummus", True, "Local Organic Hummus")
ngo_manager.add_ngo("Humanitarian Relief", "UK", "https://relief.org")
