import os
from datetime import date
from decimal import Decimal, InvalidOperation

from dotenv import load_dotenv
from supabase import create_client


def connect_to_supabase():
    """Load credentials and connect to Supabase."""
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        print("Error: SUPABASE_URL or SUPABASE_KEY is missing from .env.")
        return None

    try:
        client = create_client(url, key)

        # Test that the application can read both required tables.
        client.table("customers").select("customer_id").limit(1).execute()
        client.table("products").select("product_id").limit(1).execute()

        print("Connected to Supabase successfully.")
        return client

    except Exception as error:
        print("Could not connect or read the required tables.")
        print("Details:", error)
        return None


def get_customers(supabase):
    """Retrieve and display customers."""
    try:
        response = (
            supabase.table("customers")
            .select("customer_id, name, email, city")
            .order("customer_id")
            .execute()
        )
        customers = response.data or []

        if not customers:
            print("No customers were returned by Supabase.")
            return []

        print("\n--- CUSTOMERS ---")
        for customer in customers:
            print(
                f"ID: {customer['customer_id']} | "
                f"Name: {customer['name']} | "
                f"Email: {customer.get('email') or 'N/A'} | "
                f"City: {customer.get('city') or 'N/A'}"
            )

        return customers

    except Exception as error:
        print("Error retrieving customers:", error)
        return None


def get_products(supabase):
    """Retrieve and display products."""
    try:
        response = (
            supabase.table("products")
            .select("product_id, product_name, category, price")
            .order("product_id")
            .execute()
        )
        products = response.data or []

        if not products:
            print("No products were returned by Supabase.")
            return []

        print("\n--- PRODUCTS ---")
        for product in products:
            print(
                f"ID: {product['product_id']} | "
                f"Product: {product['product_name']} | "
                f"Category: {product.get('category') or 'N/A'} | "
                f"Price: ${Decimal(str(product['price'])):,.2f}"
            )

        return products

    except Exception as error:
        print("Error retrieving products:", error)
        return None


def get_positive_integer(prompt):
    """Accept only a positive whole number."""
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)
            if number > 0:
                return number
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Invalid entry. Please enter a whole number.")


def confirm_order():
    """Ask the user to confirm the order."""
    while True:
        answer = input("\nSave this order? (Y/N): ").strip().upper()

        if answer in ("Y", "N"):
            return answer == "Y"

        print("Please enter Y or N.")


def enter_order(supabase, customers, products):
    """Validate selections, insert an order, and verify the saved record."""
    customer_ids = {int(c["customer_id"]) for c in customers}
    product_lookup = {
        int(p["product_id"]): p for p in products
    }

    print("\n--- NEW ORDER ---")

    customer_id = get_positive_integer("Enter customer ID: ")
    if customer_id not in customer_ids:
        print("That customer ID does not exist in the displayed customer list.")
        return

    product_id = get_positive_integer("Enter product ID: ")
    if product_id not in product_lookup:
        print("That product ID does not exist in the displayed product list.")
        return

    quantity = get_positive_integer("Enter quantity: ")

    product = product_lookup[product_id]
    unit_price = Decimal(str(product["price"]))
    total = unit_price * quantity

    customer = next(
        c for c in customers if int(c["customer_id"]) == customer_id
    )

    print("\n--- ORDER SUMMARY ---")
    print(f"Customer: {customer['name']} (ID: {customer_id})")
    print(f"Product: {product['product_name']} (ID: {product_id})")
    print(f"Quantity: {quantity}")
    print(f"Unit price: ${unit_price:,.2f}")
    print(f"Order total: ${total:,.2f}")
    print(f"Order date: {date.today().isoformat()}")

    if not confirm_order():
        print("Order cancelled. Nothing was saved.")
        return

    # Use the price and date at the time the order is entered.
    order_data = {
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "order_date": date.today().isoformat(),
        "unit_price": float(unit_price),
    }

    try:
        # A single insert attempt avoids accidentally creating duplicates.
        response = (
            supabase.table("orders")
            .insert(order_data)
            .execute()
        )

        saved_rows = response.data or []

        if not saved_rows:
            print(
                "The insert returned no order record. "
                "Check Supabase before trying again."
            )
            return

        saved_order = saved_rows[0]
        order_id = saved_order.get("order_id")

        if order_id is None:
            print("Order may have been saved, but no order ID was returned.")
            print("Check the orders table before trying again.")
            return

        print("\nOrder submitted. Verifying saved order...")

        # Retrieve the saved order by its database-generated ID.
        verify_response = (
            supabase.table("orders")
            .select(
                "order_id, customer_id, product_id, quantity, "
                "order_date, unit_price"
            )
            .eq("order_id", order_id)
            .execute()
        )

        verified_rows = verify_response.data or []

        if not verified_rows:
            print(
                "The order was inserted, but verification returned no row. "
                "Check Supabase; do not submit it again yet."
            )
            return

        verified = verified_rows[0]
        verified_total = (
            Decimal(str(verified["unit_price"]))
            * int(verified["quantity"])
        )

        print("\n--- VERIFIED ORDER ---")
        print(f"Order ID: {verified['order_id']}")
        print(f"Customer ID: {verified['customer_id']}")
        print(f"Product ID: {verified['product_id']}")
        print(f"Quantity: {verified['quantity']}")
        print(f"Unit price: ${Decimal(str(verified['unit_price'])):,.2f}")
        print(f"Order total: ${verified_total:,.2f}")
        print(f"Order date: {verified['order_date']}")
        print("Verification successful.")

    except Exception as error:
        print("\nAn error occurred while saving or verifying the order.")
        print("Details:", error)
        print(
            "Check the orders table in Supabase before retrying, "
            "because the order may already have been inserted."
        )


def main():
    """Run the terminal-based order-entry application."""
    print("================================")
    print("       ORDER ENTRY SYSTEM")
    print("================================")

    supabase = connect_to_supabase()
    if supabase is None:
        return

    while True:
        customers = get_customers(supabase)
        if customers is None:
            print("Unable to load customers. Exiting.")
            return
        if not customers:
            print("Cannot enter an order without customers.")
            return

        products = get_products(supabase)
        if products is None:
            print("Unable to load products. Exiting.")
            return
        if not products:
            print("Cannot enter an order without products.")
            return

        enter_order(supabase, customers, products)

        again = input("\nEnter another order? (Y/N): ").strip().upper()
        if again != "Y":
            print("Thank you for using the Order Entry System.")
            break


if __name__ == "__main__":
    main()