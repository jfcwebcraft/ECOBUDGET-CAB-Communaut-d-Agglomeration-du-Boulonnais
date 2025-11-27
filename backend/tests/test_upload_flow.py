import requests
import os

# Create a dummy CSV file
csv_content = """Exercice,N° Bordereau,N° Pièce,Libellé,Montant HT,Nature,Fonction
2024,100,1,Achat fournitures,100.00,6064,020
2024,100,2,Frais de personnel,5000.00,6411,020
"""
with open("test_upload.csv", "w", encoding="utf-8") as f:
    f.write(csv_content)

url = "http://localhost:8000/api/v1/upload"
files = {'file': ('test_upload.csv', open('test_upload.csv', 'rb'), 'text/csv')}

print("Uploading file...")
try:
    response = requests.post(url, files=files)
    print(f"Upload Status: {response.status_code}")
    if response.status_code == 200:
        print("Upload Response:", response.json())
    else:
        print("Upload Failed:", response.text)
        exit(1)
except Exception as e:
    print(f"Upload Error: {e}")
    exit(1)

print("\nVerifying data persistence...")
url_get = "http://localhost:8000/api/v1/budget-lines"
try:
    response = requests.get(url_get)
    print(f"Get Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Retrieved {len(data)} lines.")
        print(data)
        if len(data) >= 2:
            print("SUCCESS: Data persisted correctly.")
        else:
            print("FAILURE: Data not found.")
    else:
        print("Get Failed:", response.text)
except Exception as e:
    print(f"Get Error: {e}")
