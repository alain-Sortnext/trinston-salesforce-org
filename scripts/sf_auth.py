import urllib.request, urllib.parse, os, re, sys, json

username        = os.environ.get("SF_USERNAME", "")
pw_token        = os.environ.get("SF_PASSWORD_WITH_TOKEN", "")
consumer_key    = os.environ.get("SF_CONSUMER_KEY", "")
consumer_secret = os.environ.get("SF_CONSUMER_SECRET", "")
instance_url    = os.environ.get("SF_INSTANCE_URL", "https://login.salesforce.com")

summary_file = os.environ.get("GITHUB_STEP_SUMMARY", "/tmp/step_summary.md")

def log(msg):
    print(msg)
    with open(summary_file, "a") as f:
        f.write(msg + "\n")

log(f"## Auth Attempt")
log(f"Username: `{username}`")
log(f"Instance: `{instance_url}`")
log(f"Consumer key prefix: `{consumer_key[:20]}...`")
log(f"Password+token length: `{len(pw_token)}`")

for url in [
    f"{instance_url}/services/oauth2/token",
    "https://login.salesforce.com/services/oauth2/token",
]:
    log(f"\n### Trying: {url}")
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
                log(f"**SUCCESS**: {inst_url}")
                sfdx_url = f"force://{consumer_key}:{consumer_secret}:{token}@{inst_url.replace('https://','')}"
                with open("/tmp/sfdx_auth_url.txt", "w") as f:
                    f.write(sfdx_url)
                sys.exit(0)
            else:
                log(f"**No token**: {json.dumps(resp)}")
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        log(f"**HTTP {e.code}**: ```{err[:500]}```")
    except Exception as ex:
        log(f"**Exception**: {type(ex).__name__}: {ex}")

log("\n**All attempts failed**")
sys.exit(1)
