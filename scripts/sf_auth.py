import urllib.request, urllib.parse, os, sys, json

username        = os.environ.get("SF_USERNAME", "")
pw_token        = os.environ.get("SF_PASSWORD_WITH_TOKEN", "")
consumer_key    = os.environ.get("SF_CONSUMER_KEY", "")
consumer_secret = os.environ.get("SF_CONSUMER_SECRET", "")
summary         = os.environ.get("GITHUB_STEP_SUMMARY", "/dev/null")

def log(msg):
    print(msg)
    open(summary, "a").write(msg + "\n")

log(f"Authenticating: {username}")
url = "https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com/services/oauth2/token"

data = urllib.parse.urlencode({
    "grant_type": "password", "client_id": consumer_key,
    "client_secret": consumer_secret, "username": username, "password": pw_token,
}).encode()

try:
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=30) as r:
        resp = json.loads(r.read())
        if "access_token" not in resp:
            log(f"FAIL: {resp}")
            sys.exit(1)
        token    = resp["access_token"]
        inst_url = resp["instance_url"]
        log(f"SUCCESS: {inst_url}")

    # Save for data loading
    os.makedirs("/tmp/sf", exist_ok=True)
    open("/tmp/sf/token", "w").write(token)
    open("/tmp/sf/instance", "w").write(inst_url)

    # Write SFDX URL for sf cli login
    sfdx_url = f"force://{consumer_key}:{consumer_secret}:{token}@{inst_url.replace('https://','')}"
    open("/tmp/sfdx_auth_url.txt","w").write(sfdx_url)
    log("Credentials saved")
    sys.exit(0)

except urllib.error.HTTPError as e:
    log(f"HTTP {e.code}: {e.read().decode()[:300]}")
    sys.exit(1)
except Exception as ex:
    log(f"{type(ex).__name__}: {ex}")
    sys.exit(1)
