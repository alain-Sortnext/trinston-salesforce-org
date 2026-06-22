import urllib.request, urllib.parse, json, csv, os, sys

token    = open("/tmp/sf/token").read().strip()
instance = open("/tmp/sf/instance").read().strip()
api      = f"{instance}/services/data/v59.0"

def sf_post(endpoint, records):
    """POST to Salesforce Composite API - batch of 200"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    results = {"success": 0, "fail": 0}
    
    for i in range(0, len(records), 200):
        batch = records[i:i+200]
        body = {"allOrNone": False, "records": [{"attributes": {"type": r["_type"]}, **{k:v for k,v in r.items() if not k.startswith("_")}} for r in batch]}
        req = urllib.request.Request(f"{api}/composite/sobjects", data=json.dumps(body).encode(), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as r:
            resp = json.loads(r.read())
            for item in resp:
                if item.get("success"): results["success"] += 1
                else: results["fail"] += 1
        print(f"  Batch {i//200+1}: {results}")
    return results

# Load Accounts
sobject = sys.argv[1]
csv_file = sys.argv[2]
sf_type  = sys.argv[3]
required_fields = sys.argv[4:] if len(sys.argv) > 4 else []

records = []
with open(csv_file, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        r = {"_type": sf_type}
        for k, v in row.items():
            if v and v.strip():
                r[k] = v.strip()
        # Check required fields
        if all(r.get(f) for f in required_fields):
            records.append(r)

print(f"Loading {len(records)} {sf_type} records...")
if records:
    result = sf_post(f"/composite/sobjects", records)
    print(f"Done: {result}")
    
    # Count in org
    req = urllib.request.Request(f"{api}/query?q=SELECT+COUNT()+FROM+{sf_type}", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as r:
        count = json.loads(r.read())["totalSize"]
    print(f"Total {sf_type} in org: {count}")
