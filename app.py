from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# 1. Setup Google Sheets Authentication
# You'll need a 'credentials.json' file from Google Cloud Console
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("TinyUniquon order management")

@app.route('/fetch-designs', methods=['GET'])
def fetch_designs():
    age = request.args.get('age')
    gender = request.args.get('gender')
    inventory = sheet.worksheet("Sheet1").get_all_records()
    
    # Filter designs based on user input
    matching_designs = [row['Design'] for row in inventory if row['Age'] == age and row['Gender'] == gender]
    return jsonify(matching_designs)

@app.route('/place-order', methods=['POST'])
def place_order():
    data = request.json
    order_sheet = sheet.worksheet("Orders")
    
    # Add a new row to the sheet
    order_sheet.append_row([
        data.get('name'), 
        data.get('phone'), 
        data.get('design'), 
        data.get('quantity'), 
        int(data.get('quantity')) * 500
    ])
    return "Order Placed", 200

if __name__ == '__main__':
    app.run(port=5000)