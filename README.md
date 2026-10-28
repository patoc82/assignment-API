# assignment-API

# Supabase Order Entry

## Project Description

### This project is a Python terminal application that allows users to create orders for existing customers using a Supabase database.

### The program retrieves customers and products from Supabase, validates user input, displays an order summary, requests confirmation, inserts the order, and queries Supabase again to verify that the order was saved.

### Each order contains one product and can include multiple units.

## Database Tables

### The program uses these existing Supabase tables:

### - customers: customer_id, name, email, city
### - products: product_id, product_name, category, price
### - orders: order_id, customer_id, product_id, quantity,
  order_date, unit_price

The database generates the order ID.

## Requirements

### - Python 3
### - A Supabase project with the required tables
### - A Supabase URL and an appropriate API key
### - The packages listed in requirements.txt

## Setup Instructions

### 1. Clone or download this repository.
### 2. Open the project folder in VS Code.
### 3. Create a virtual environment:

   ### python3 -m venv .venv

### 4. Activate it on macOS:

   #### source .venv/bin/activate

### 5. Install the required packages:

   #### python -m pip install -r requirements.txt

### 6. Copy .env.example to a new file named .env.
### 7. Add your own Supabase URL and publishable or anon key to .env.
### 8. Confirm that the key and database permissions allow the required reads and order insertions.

#### Never commit the real .env file or secret credentials.

## How to Run

### Open the VS Code terminal in the project folder and run:

#### python order_entry.py

## Program Features

### - Retrieves and displays existing customers and products.
### - Displays product prices to two decimal places.
### - Validates customer IDs and product IDs.
### - Requires a positive whole-number quantity.
### - Rejects invalid input and prompts the user again.
### - Displays the customer, product, quantity, unit price,
  and order total before confirmation.
- Accepts uppercase and lowercase Y/N responses.
- Cancels an order without inserting a record when N is selected.
- Inserts confirmed orders through the Supabase API.
- Saves the current date and selected product price.
- Uses the database-generated order ID.
- Queries Supabase again to retrieve the saved order.
- Calculates the verified total using the stored unit price.
- Allows the user to enter multiple orders in one session.
- Does not automatically retry a potentially successful insertion.

## Testing Results

### Complete this table after running each test. Record the actual outcome and do not mark a test as passed unless you have verified it.

### | Test | Actual result |
### |---|---|
### | Text instead of customer ID | Fill in after testing |
### | Unknown customer ID | Fill in after testing |
### | Unknown product ID | Fill in after testing |
### | Quantity 0 | Fill in after testing |
### | Quantity -2 | Fill in after testing |
### | Quantity 1.5 | Fill in after testing |
### | Quantity hello | Fill in after testing |
### | Invalid confirmation response | Fill in after testing |
### | Cancelled order | Fill in after testing |
### | Successful insertion | Fill in after testing |
### | Separate verification query | Fill in after testing |
### | Multiple orders in one session | Fill in after testing |

## Evidence

### Include terminal screenshots or copied terminal output demonstrating a successful order insertion and the subsequent verification query.

### Make sure all evidence excludes credentials.

## Libraries and References

### The project uses third-party Python libraries for connecting to Supabase and loading environment variables.

### - Supabase Python client:
  https://supabase.com/docs/reference/python/introduction
- Supabase API keys and security:
  https://supabase.com/docs/guides/api/api-keys
- python-dotenv:
  https://pypi.org/project/python-dotenv/

Python standard-library modules used include os, datetime,
and decimal.

## Security

### The .env file contains private local configuration and must not be committed to GitHub. The .env.example file contains placeholders only. Use an appropriate API key and configure database permissions according to the assignment requirements.