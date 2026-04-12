import urllib.request, json, urllib.parse

req = urllib.request.Request(
    "http://localhost:8000/api/risks/", 
    data=json.dumps({"assessment_id": "RSK-test-1", "patient_id": "PT-001", "risk_score": 50, "category": "Low"}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
urllib.request.urlopen(req)

res = urllib.request.urlopen("http://localhost:8000/api/patients/PT-001")
data = json.loads(res.read())
print(f"Risks length: {len(data['risks'])}")
