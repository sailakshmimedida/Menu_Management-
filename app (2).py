import streamlit as st
import datetime

# ----------------- OOP CLASSES -----------------
class MenuItem:
    def __init__(self, item_id, name, price, available=True):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.available = available

class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_id):
        self.items = [item for item in self.items if item.item_id != item_id]

    def update_item(self, item_id, new_name=None, new_price=None, available=None):
        for item in self.items:
            if item.item_id == item_id:
                if new_name:
                    item.name = new_name
                if new_price:
                    item.price = new_price
                if available is not None:
                    item.available = available
                return True
        return False

    def display_menu(self):
        return self.items

    def get_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                return item
        return "NOT_FOUND"

class Order:
    def __init__(self):
        self.ordered_items = []

    def add_to_order(self, item, quantity):
        self.ordered_items.append((item, quantity))

    def display_order(self):
        total = 0
        bill_lines = []
        for item, qty in self.ordered_items:
            subtotal = item.price * qty
            total += subtotal
            bill_lines.append(f"{item.name} x {qty} = ₹{subtotal}")
        return bill_lines, total

# ----------------- INITIAL DATA -----------------
def create_menu():
    menu = Menu()
    sample_items = [
        ("Pizza", 350), ("Burger", 150), ("Pasta", 250), ("Biryani", 300), ("Sandwich", 120),
        ("Fried Rice", 200), ("Noodles", 220), ("Dosa", 100), ("Idli", 80), ("Paratha", 90),
        ("Coffee", 60), ("Tea", 40), ("Juice", 100), ("Ice Cream", 150), ("Cake", 200),
        ("Soup", 180), ("Salad", 170), ("French Fries", 130), ("Paneer Tikka", 250), ("Chicken Curry", 400),
        ("Fish Fry", 350), ("Egg Curry", 220), ("Veg Pulao", 200), ("Samosa", 50), ("Pakora", 70),
        ("Spring Roll", 120), ("Shawarma", 180), ("Momos", 160), ("Cutlet", 90), ("Maggi", 80),
        ("Thali", 300), ("Poori", 110), ("Upma", 90), ("Pongal", 100), ("Vada", 70),
        ("Cold Coffee", 120), ("Milkshake", 150), ("Falooda", 180), ("Brownie", 170), ("Donut", 100),
        ("Sandesh", 200), ("Rasgulla", 180), ("Gulab Jamun", 150), ("Kachori", 90), ("Pav Bhaji", 160),
        ("Chole Bhature", 180), ("Rajma Chawal", 220), ("Dal Makhani", 250), ("Butter Naan", 50), ("Roti", 20),
        ("Panner Butter Masala", 280), ("Chicken Biryani", 450), ("Mutton Curry", 500), ("Fish Curry", 480), ("Veg Manchurian", 220)
    ]
    for idx, (name, price) in enumerate(sample_items, start=1):
        menu.add_item(MenuItem(idx, name, price))
    return menu

# ----------------- STREAMLIT APP -----------------
st.set_page_config(page_title="Menu Management System", layout="wide")
st.title("🍽️ Menu Management System")

if "menu" not in st.session_state:
    st.session_state.menu = create_menu()

if "order" not in st.session_state:
    st.session_state.order = Order()

mode = st.sidebar.radio("Choose Mode:", ["Customer", "Admin"])

# ----------------- CUSTOMER MODE -----------------
if mode == "Customer":
    st.subheader("📋 Menu")

    # 🔍 Search bar
    search_query = st.text_input("Search for an item (e.g., Pizza, Biryani, Coffee)")

    # Filter items
    filtered_items = [
        item for item in st.session_state.menu.display_menu()
        if search_query.lower() in item.name.lower()
    ] if search_query else st.session_state.menu.display_menu()

    if not filtered_items:
        st.warning("❌ No items found. Try another search.")
    else:
        for item in filtered_items:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{item.name}** - ₹{item.price}" + ("" if item.available else " ❌ (Not Available)"))
            with col2:
                if item.available:
                    qty = st.number_input(f"Qty", min_value=0, max_value=10, step=1, key=f"qty_{item.item_id}")
                    if st.button(f"Add {item.name}", key=f"btn_{item.item_id}"):
                        if qty > 0:
                            st.session_state.order.add_to_order(item, qty)
                            st.success(f"✅ {item.name} x {qty} added to order!")
                        else:
                            st.warning("Quantity must be greater than 0.")
                else:
                    st.write("❌ Unavailable")

    # ----------------- ORDER SUMMARY -----------------
    st.subheader("🧾 Your Order")
    if st.session_state.order.ordered_items:
        bill_lines, total = st.session_state.order.display_order()
        for line in bill_lines:
            st.write(line)

        # 🚨 Day-based Discount
        today = datetime.datetime.today().strftime("%A")  # e.g. "Sunday"
        if total > 2500 and today in ["Sunday", "Wednesday"]:
            discount = total * 0.10
            final_amount = total - discount
            st.write(f"### 💰 Total Bill: ₹{total}")
            st.success(f"🎉 Special {today} Offer! 10% discount of ₹{discount:.2f}")
            st.write(f"### 🏷️ Final Amount to Pay: ₹{final_amount:.2f}")
        else:
            st.write(f"### 💰 Total Bill: ₹{total}")
            if total > 2500:
                st.info("👉 Discount is available only on Sunday & Wednesday.")
    else:
        st.info("No items ordered yet.")

# ----------------- ADMIN MODE -----------------
else:
    st.subheader("⚙️ Admin Panel")
    action = st.radio("Action", ["View Menu", "Add Item", "Update Item", "Remove Item"])

    if action == "View Menu":
        st.write("### Current Menu")
        for item in st.session_state.menu.display_menu():
            st.write(f"{item.item_id}. {item.name} - ₹{item.price}" + ("" if item.available else " ❌ Unavailable"))

    elif action == "Add Item":
        name = st.text_input("Enter item name")
        price = st.number_input("Enter price", min_value=1)
        if st.button("Add"):
            item_id = len(st.session_state.menu.items) + 1
            st.session_state.menu.add_item(MenuItem(item_id, name, price))
            st.success(f"✅ {name} added to the menu.")

    elif action == "Update Item":
        item_id = st.number_input("Enter Item ID to update", min_value=1, step=1)
        new_name = st.text_input("Enter new name (leave blank if no change)")
        new_price = st.number_input("Enter new price (leave 0 if no change)", min_value=0)
        available = st.selectbox("Available?", ["No Change", "Yes", "No"])
        if st.button("Update"):
            availability = None if available == "No Change" else (True if available == "Yes" else False)
            if st.session_state.menu.update_item(item_id, new_name if new_name else None, new_price if new_price > 0 else None, availability):
                st.success("✅ Item updated successfully.")
            else:
                st.error("❌ Item not found.")

    elif action == "Remove Item":
        item_id = st.number_input("Enter Item ID to remove", min_value=1, step=1)
        if st.button("Remove"):
            st.session_state.menu.remove_item(item_id)
            st.success("✅ Item removed successfully.")
