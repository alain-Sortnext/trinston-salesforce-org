import urllib.request, urllib.parse, os, sys, json

username        = os.environ.get("SF_USERNAME", "")
pw_token        = os.environ.get("SF_PASSWORD_WITH_TOKEN", "")
consumer_key    = os.environ.get("SF_CONSUMER_KEY", "")
consumer_secret = os.environ.get("SF_CONSUMER_SECRET", "")
instance_url    = "https://orgfarm-709b3a2059-dev-ed.develop.my.salesforce.com"

summary = os.environ.get("GITHUB_STEP_SUMMARY", "/tmp/summary.md")

def log(msg):
    print(msg)
    with open(summary, "a") as f:
        f.write(msg + "\n")

log(f"Username: {username}")
log(f"Instance: {instance_url}")
log(f"PW+Token length: {len(pw_token)}")

url = f"{instance_url}/services/oauth2/token"
log(f"Trying: {url}")

data = urllib.parse.urlencode({
    "grant_type":    "password",
    "client_id":     consumer_key,
    "client_secret": consumer_secret,
    "username":      username,
    "password":      pw_token,
}).encode()

try:
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read())
        if "access_token" in resp:
            token    = resp["access_token"]
            inst_url = resp["instance_url"]
            log(f"SUCCESS: {inst_url}")
            sfdx_url = f"force://{consumer_key}:{consumer_secret}:{token}@{inst_url.replace('https://','')}"
            with open("/tmp/sfdx_auth_url.txt", "w") as f:
                f.write(sfdx_url)
            sys.exit(0)
        else:
            log(f"No token: {json.dumps(resp)}")
            sys.exit(1)
except urllib.error.HTTPError as e:
    err = e.read().decode()
    log(f"HTTP {e.code}: {err[:500]}")
    sys.exit(1)
except Exception as ex:
    log(f"{type(ex).__name__}: {ex}")
    sys.exit(1)
