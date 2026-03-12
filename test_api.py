import requests

url = "https://myoperator.onrender.com/place-order"
data = {
    "name": "Test User",
    "phone": "1234567890",
    "design": "BD21",
    "quantity": "2"
}

response = requests.post(url, json=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")