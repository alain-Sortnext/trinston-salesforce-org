import urllib.request, urllib.parse, os, sys, json

username        = os.environ.get("SF_USERNAME", "")
password_only   = os.environ.get("SF_PASSWORD", "")
pw_token        = os.environ.get("SF_PASSWORD_WITH_TOKEN", "")
consumer_key    = os.environ.get("SF_CONSUMER_KEY", "")
consumer_secret = os.environ.get("SF_CONSUMER_SECRET", "")
summary         = os.environ.get("GITHUB_STEP_SUMMARY", "/dev/null")

ORG_URL = "https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com"

def log(msg):
    print(msg)
    open(summary, "a").write(msg + "\n")

def try_auth(password_str, label):
    url = f"{ORG_URL}/services/oauth2/token"
    data = urllib.parse.urlencode({
        "grant_type": "password",
        "client_id": consumer_key,
        "client_secret": consumer_secret,
        "username": username,
        "password": password_str,
    }).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=30) as r:
            resp = json.loads(r.read())
            if "access_token" in resp:
                log(f"SUCCESS [{label}]: {resp['instance_url']}")
                return resp["access_token"], resp["instance_url"]
            log(f"FAIL [{label}]: {resp}")
            return None, None
    except urllib.error.HTTPError as e:
        log(f"HTTP {e.code} [{label}]: {e.read().decode()[:200]}")
        return None, None

log(f"Username: {username}")
log(f"PW-only length: {len(password_only)}")
log(f"PW+token length: {len(pw_token)}")

# Try password only first (IP is relaxed - token not needed)
token, inst = try_auth(password_only, "password only")

# Fallback: password + token
if not token:
    token, inst = try_auth(pw_token, "password+token")

if not token:
    log("All attempts failed")
    sys.exit(1)

# Save credentials
os.makedirs("/tmp/sf", exist_ok=True)
open("/tmp/sf/token", "w").write(token)
open("/tmp/sf/instance", "w").write(inst)

# Write SFDX URL
sfdx_url = f"force://{consumer_key}:{consumer_secret}:{token}@{inst.replace('https://','')}"
open("/tmp/sfdx_auth_url.txt","w").write(sfdx_url)
log("Done")
sys.exit(0)
