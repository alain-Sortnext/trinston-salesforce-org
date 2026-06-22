import urllib.request, urllib.parse, os, re, sys, json

username      = os.environ.get("SF_USERNAME", "")
pw_token      = os.environ.get("SF_PASSWORD_WITH_TOKEN", "")
consumer_key  = os.environ.get("SF_CONSUMER_KEY", "")
consumer_secret = os.environ.get("SF_CONSUMER_SECRET", "")
instance_url  = os.environ.get("SF_INSTANCE_URL", "https://login.salesforce.com")

print(f"Username: {username}")
print(f"Instance: {instance_url}")

# Try OAuth2 password grant via the org's own token endpoint
for url in [
    f"{instance_url}/services/oauth2/token",
    "https://login.salesforce.com/services/oauth2/token",
]:
    print(f"Trying: {url}")
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
                print(f"SUCCESS: {inst_url}")
                sfdx_url = f"force://{consumer_key}:{consumer_secret}:{token}@{inst_url.replace('https://','')}"
                with open("/tmp/sfdx_auth_url.txt", "w") as f:
                    f.write(sfdx_url)
                print("SFDX URL written")
                sys.exit(0)
            else:
                print(f"No token: {resp}")
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"HTTP {e.code}: {err[:300]}")
    except Exception as ex:
        print(f"{type(ex).__name__}: {ex}")

print("All attempts failed")
sys.exit(1)
