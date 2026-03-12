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

    matching_designs = [
        row['Design'] for row in inventory
        if row['Age'] == age and row['Gender'] == gender
    ]

    return jsonify(matching_designs)


@app.route('/place-order', methods=['POST'])
def place_order():
    data = request.json
    order_sheet = sheet.worksheet("Orders")

    order_sheet.append_row([
        data.get('name'),
        data.get('phone'),
        data.get('design'),
        data.get('quantity'),
        int(data.get('quantity')) * 500
    ])

    return "Order Placed", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)