import streamlit as st
from database.product_manager import ProductManager

product_db = ProductManager()

def scan_and_check(search_term):
    term = search_term.strip().lower()
    product = product_db.search_product(term)

    if product:
        pid, barcode, name, brand, is_israeli, alt_id = product
        alt_product = product_db.get_product_by_id(alt_id) if alt_id else None
        return {
            "barcode": barcode,
            "product": {
                "product_name": name,
                "brand": brand
            },
            "is_israeli": bool(is_israeli),
            "alt_product": {
                "product_name": alt_product[2],
                "brand": alt_product[3]
            } if alt_product else None,
            "product_found": True
        }
    else:
        return {
            "barcode": term,
            "product": {
                "product_name": "Unknown",
                "brand": "Unknown"
            },
            "is_israeli": False,
            "alt_product": None,
            "product_found": False
        }

class ProductCheckerUI:
    def __init__(self):
        self.title = "Manual Product Checker"

    def run(self):
        st.title(self.title)
        search_term = st.text_input("Enter barcode, product name, or brand")

        if st.button("Check Product"):
            if not search_term.strip():
                st.warning("Please enter a search term.")
                return

            result = scan_and_check(search_term)
            name = result["product"]["product_name"]
            brand = result["product"]["brand"]

            if not result["product_found"]:
                st.warning("⚠️ Product not found.")
            else:
                st.markdown(f"**🔎 Product:** {name}")
                st.markdown(f"**🏷️ Brand:** {brand}")

                if result["is_israeli"]:
                    st.error("🚨 Warning: This is an Israeli brand!")
                    if result["alt_product"]:
                        alt = result["alt_product"]
                        st.markdown("---")
                        st.markdown("### ✅ Alternative Suggested:")
                        st.markdown(f"**🛍️ Product:** {alt['product_name']}")
                        st.markdown(f"**🏷️ Brand:** {alt['brand']}")
                else:
                    st.success("✅ This brand seems safe.")

if __name__ == "__main__":
    ui = ProductCheckerUI()
    ui.run()
