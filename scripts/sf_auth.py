import urllib.request, urllib.parse, os, sys, json

username        = os.environ.get("SF_USERNAME", "")
pw_token        = os.environ.get("SF_PASSWORD_WITH_TOKEN", "")
consumer_key    = os.environ.get("SF_CONSUMER_KEY", "")
consumer_secret = os.environ.get("SF_CONSUMER_SECRET", "")
summary         = os.environ.get("GITHUB_STEP_SUMMARY", "/dev/null")

def log(msg):
    print(msg)
    open(summary, "a").write(msg + "\n")

url = "https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com/services/oauth2/token"
data = urllib.parse.urlencode({
    "grant_type": "password", "client_id": consumer_key,
    "client_secret": consumer_secret, "username": username, "password": pw_token,
}).encode()

with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=30) as r:
    resp = json.loads(r.read())
    token    = resp["access_token"]
    inst_url = resp["instance_url"]
    log(f"OAuth SUCCESS: {inst_url}")

# Save token and instance for data loading script
os.makedirs("/tmp/sf", exist_ok=True)
with open("/tmp/sf/token", "w") as f: f.write(token)
with open("/tmp/sf/instance", "w") as f: f.write(inst_url)

# Login SF CLI
sfdx_url = f"force://{consumer_key}:{consumer_secret}:{token}@{inst_url.replace('https://','')}"
open("/tmp/sfdx_auth_url.txt","w").write(sfdx_url)
open("/tmp/use_sfdx_url","w").write("yes")
log("Credentials saved for data load")
