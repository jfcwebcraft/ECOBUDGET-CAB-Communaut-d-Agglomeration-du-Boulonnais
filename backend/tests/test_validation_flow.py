import requests
import json

# 1. Upload File
url_upload = "http://localhost:8000/api/v1/upload"
files = {'file': ('test_val.csv', 'Exercice,N° Bordereau,N° Pièce,Libellé,Montant HT,Nature,Fonction\n2024,200,1,Test Validation,100.00,6064,020', 'text/csv')}
print("Uploading...")
requests.post(url_upload, files=files)

# 2. Get Line to find ID
url_get = "http://localhost:8000/api/v1/budget-lines"
resp = requests.get(url_get)
data = resp.json()
target_line = next((l for l in data if l['num_bordereau'] == 200), None)

if not target_line:
    print("FAILURE: Line not found")
    exit(1)

print(f"Found line: {target_line['statut']}")

# 3. Validate
print("Validating...")
url_update = f"http://localhost:8000/api/v1/budget-lines/{target_line['exercice']}/{target_line['num_bordereau']}/{target_line['num_piece']}"
resp = requests.put(url_update, json={"statut": "VALIDE"})
if resp.status_code != 200:
    print(f"FAILURE: Validation failed {resp.text}")
    exit(1)

print(f"Validation Response: {resp.json()['statut']}")

# 4. Correct
print("Correcting...")
correction_data = {
    "cotation_axe1": "FAVORABLE",
    "justification_axe1": "Correction manuelle",
    "statut": "VALIDE"
}
resp = requests.put(url_update, json=correction_data)
if resp.status_code != 200:
    print(f"FAILURE: Correction failed {resp.text}")
    exit(1)

updated_line = resp.json()
print(f"Correction Response: Cotation={updated_line['cotation_axe1']}, Justif={updated_line['justification_axe1']}")

if updated_line['cotation_axe1'] == "FAVORABLE" and updated_line['statut'] == "VALIDE":
    print("SUCCESS: Validation and Correction flow verified.")
else:
    print("FAILURE: Data mismatch.")
