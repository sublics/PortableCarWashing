import streamlit as st
import json
import requests

# Define the webhook URL
webhook_url = "https://hooks.zapier.com/hooks/catch/21732373/2wrfv1u/"

# Define a function to send a notification to the webhook
def send_notification(customer_info):
    data = {"customer_info": customer_info}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print("Error sending notification:", response.text)

# Define a function to add a customer and send a notification
def add_customer(new_customer):
    send_notification(new_customer)

# Load the individual numbers from the file
def load_individual_numbers():
    try:
        with open('individual_numbers.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save the individual numbers to the file
def save_individual_numbers(numbers):
    with open('individual_numbers.json', 'w') as f:
        json.dump(numbers, f)

# Load the customer information list from the file
def load_customer_info():
    try:
        with open('customer_info.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save the customer information list to the file
def save_customer_info(customer_info):
    with open('customer_info.json', 'w') as f:
        json.dump(customer_info, f)

# Create a login page
def login_page():
    st.title("Login Page")
    user_type = st.selectbox("Select User Type", ["Admin", "Individual"])
    if user_type == "Admin":
        admin_login()
    elif user_type == "Individual":
        individual_login()

# Create an admin login page
def admin_login():
    st.title("Admin Login")
    admin_name = st.text_input("Admin Name")
    admin_phone = st.text_input("Admin Phone Number")
    if admin_name == "Saud Alsaud" and admin_phone == "0568315055":
        st.session_state["logged_in"] = True
        st.session_state["user_type"] = "Admin"
        st.session_state["admin_name"] = admin_name
        st.session_state["admin_phone"] = admin_phone
        main_page()

# Create an individual login page
def individual_login():
    st.title("Individual Login")
    individual_number = st.text_input("Individual Number")
    individual_numbers = load_individual_numbers()
    if individual_number in individual_numbers:
        st.session_state["logged_in"] = True
        st.session_state["user_type"] = "Individual"
        st.session_state["individual_number"] = individual_number
        main_page()
    else:
        st.error("Invalid individual credentials")

# Create a main page for the app
def main_page():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if st.session_state["logged_in"]:
        st.title("Portable Car Wash App")
        if st.session_state["user_type"] == "Admin":
            admin_page()
        elif st.session_state["user_type"] == "Individual":
            individual_page()
    else:
        login_page()

# Create a main page for admins
def admin_page():
    st.write(f"Welcome, {st.session_state['admin_name']}!")
    st.write(f"Your phone number is: {st.session_state['admin_phone']}")

    st.title("Portable Car Wash App")
    customer_info_list = load_customer_info()
    with st.form("admin_form"):
        customer_number = st.text_input("Customer Number", max_chars=10)
        car_size = st.selectbox("Car Size", ["Large", "Medium", "Small"])
        washing_options = st.multiselect("Washing Options", [
            "Wash Inside",
            "Wash Outside",
            "Wash Inside and Outside",
            "Wash with Nano Machine",
            "Wash with Steam"
        ])
        washing_cost = st.text_input("Washing Cost")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            if customer_number and car_size and washing_options and washing_cost:
                new_customer = {
                    "Customer Number": customer_number,
                    "Car Size": car_size,
                    "Washing Options": washing_options,
                    "Washing Cost": washing_cost
                }
                customer_info_list.append(new_customer)
                save_customer_info(customer_info_list)
                add_customer(new_customer)
            else:
                st.error("Please fill in all fields")
    st.write("Customer Information List:")
    for i, customer_info in enumerate(customer_info_list):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(customer_info)
        with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    customer_info_list.pop(i)
                    save_customer_info(customer_info_list)
    st.title("Add Individual Number")
    with st.form("add_individual_form"):
        individual_number = st.text_input("Add Individual Number")
        submit_button = st.form_submit_button("Add")
        if submit_button:
            if individual_number:
                individual_numbers = load_individual_numbers()
                individual_numbers.append(individual_number)
                save_individual_numbers(individual_numbers)
                st.success("Individual number added successfully")
            else:
                st.error("Please enter an individual number")
    st.write("Individual Numbers:")
    for i, number in enumerate(load_individual_numbers()):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(number)
        with col2:
            if st.button("Remove", key=f"remove_individual_{i}"):
                individual_numbers = load_individual_numbers()
                individual_numbers.pop(i)
                save_individual_numbers(individual_numbers)

# Create a main page for individuals
def individual_page():
    st.write(f"Welcome, Individual {st.session_state['individual_number']}!")
    customer_info_list = load_customer_info()
    with st.form("individual_form"):
        customer_number = st.text_input("Customer Number", max_chars=10)
        car_size = st.selectbox("Car Size", ["Large", "Medium", "Small"])
        washing_options = st.multiselect("Washing Options", [
            "Wash Inside",
            "Wash Outside",
            "Wash Inside and Outside",
            "Wash with Nano Machine",
            "Wash with Steam"
        ])
        washing_cost = st.text_input("Washing Cost")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            customer_info_list.append({
                "Customer Number": customer_number,
                "Car Size": car_size,
                "Washing Options": washing_options,
                "Washing Cost": washing_cost
            })
            save_customer_info(customer_info_list)
            add_customer(customer_info_list)
    st.write("Customer Information List:")
    for customer_info in customer_info_list:
        st.write(customer_info)

# Run the main page
if __name__ == "__main__":
    main_page()