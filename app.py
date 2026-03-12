from flask import Flask, request, jsonify
import gspread
import os
import json
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Google Sheets authentication from environment variable
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

client = gspread.authorize(creds)
sheet = client.open("TinyUniquon order management")


@app.route('/fetch-designs', methods=['GET'])
def fetch_designs():
    age = request.args.get('age')
    gender = request.args.get('gender')

    inventory = sheet.worksheet("Sheet1").get_all_records()

    matching_designs = []

    for row in inventory:
        sheet_gender = row["Gender"].lower()
        sheet_age = row["Age"]

        if gender.lower() in sheet_gender:
            if sheet_age == "2-4 years" and 2 <= int(age) <= 4:
                matching_designs.append(row["Design"])
            elif sheet_age == "4-6 years" and 4 <= int(age) <= 6:
                matching_designs.append(row["Design"])

    return jsonify(matching_designs)


@app.route('/place-order', methods=['POST'])
def place_order():
    try:
        data = request.get_json() # Use get_json() to ensure it parses the body
        if not data:
            return "No data received", 400
            
        order_sheet = sheet.worksheet("Orders")

        # Safely handle quantity and price
        qty_str = data.get('quantity', '0')
        # This prevents the 500 error if quantity is empty or not a number
        qty = int(qty_str) if str(qty_str).isdigit() else 0
        
        price_per_unit = 500
        total_price = qty * price_per_unit

        order_sheet.append_row([
            data.get('name', 'N/A'),
            data.get('phone', 'N/A'),
            data.get('design', 'N/A'),
            qty,
            total_price
        ])

        return "Order Placed", 200
    except Exception as e:
        print(f"Error: {e}") # This will show up in your Render logs
        return str(e), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)